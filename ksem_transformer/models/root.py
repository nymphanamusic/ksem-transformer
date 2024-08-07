# pyright: reportUnknownMemberType=none, reportUnknownVariableType=none
from __future__ import annotations

import json
from collections.abc import Generator
from functools import reduce
from pathlib import Path
from typing import Annotated, Any, Literal, Protocol, Self, cast

import attrs
from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    SerializerFunctionWrapHandler,
    model_serializer,
    model_validator,
)
from ruamel.yaml import YAML as Yaml  # pyright: ignore[reportMissingTypeStubs]

from ksem_transformer.models.keyswitches import Keyswitches
from ksem_transformer.models.ksem_json_types import KsemConfig
from ksem_transformer.models.ksem_parsing import make_keyswitches
from ksem_transformer.models.settings.settings import Settings
from ksem_transformer.note import Note
from ksem_transformer.utils.tree import Tree, deep_join_trees
from ksem_transformer.utils.yaml_utils import yaml_dumps, yaml_load

KSEM_VERSION = "4.2"

type SettingsLocation = Literal["root", "product", "instrument_group", "instrument"]


class HasSettings(Protocol):
    settings: Settings


@attrs.define()
class KsemConfigFile:
    """
    Represents a KSEM configuration file with its path and data.
    """

    file: Path
    data: KsemConfig


class Container[Parent: "Container | None"](BaseModel):
    parent: Parent | None = Field(default=None, exclude=True)
    settings: Settings = Field(default_factory=Settings)

    @model_serializer(mode="wrap")
    def _serialize_main_models(
        self: HasSettings, handler: SerializerFunctionWrapHandler
    ):
        with Note.with_middle_c(self.settings.middle_c):
            partial_value = handler(self)
        if self.settings.is_default():
            del partial_value["settings"]
        return partial_value

    def get_merged_settings(self) -> Settings:
        settings_ascending: list[Settings] = [self.settings]
        obj = self
        while hasattr(obj, "parent") and obj.parent is not None:
            assert isinstance(obj, Container)
            obj = obj.parent
            settings_ascending.append(obj.settings)
        return Settings.combine(*settings_ascending[::-1])


class ChildProto[T](Protocol):
    parent: T | None


class ChildDict[K, V: ChildProto[Any], Parent](dict[K, V]):
    _parent: Parent | None = None

    @property
    def parent(self) -> Parent | None:
        return self._parent

    @parent.setter
    def parent(self, new_parent: Parent | None) -> None:
        self._parent = new_parent
        self._update_parents()

    def _update_parents(self):
        for v in self.values():
            v.parent = self.parent

    def __attrs_post_init__(self):
        self._update_parents()

    def __setitem__(self, key: K, value: V) -> None:
        value.parent = self.parent
        super().__setitem__(key, value)


class Instrument(Container["InstrumentGroup"], BaseModel):
    """
    Represents an instrument.
    """

    keyswitches: Keyswitches


class InstrumentGroup(Container["Product"], BaseModel):
    """
    Represents a group of instruments.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    instruments: Annotated[
        dict[str, Instrument],
        AfterValidator(
            lambda x: (
                ChildDict(x)
                if not isinstance(x, ChildDict)
                else cast(ChildDict[str, Instrument, InstrumentGroup], x)
            )
        ),
    ]

    @model_validator(mode="after")
    def set_parent(self) -> Self:
        cast(
            ChildDict[str, Instrument, InstrumentGroup], self.instruments
        ).parent = self
        return self


class Product(Container["Root"], BaseModel):
    """
    Represents a product.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    instrument_groups: Annotated[
        dict[str, InstrumentGroup],
        AfterValidator(
            lambda x: (
                ChildDict(x)
                if not isinstance(x, ChildDict)
                else cast(ChildDict[str, InstrumentGroup, Product], x)
            )
        ),
    ]

    @model_validator(mode="after")
    def set_parent(self) -> Self:
        cast(
            ChildDict[str, InstrumentGroup, Product], self.instrument_groups
        ).parent = self
        return self


class Root(Container[None], BaseModel):
    """
    Represents the root configuration.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    products: Annotated[
        dict[str, Product],
        AfterValidator(
            lambda x: (
                ChildDict(x)
                if not isinstance(x, ChildDict)
                else cast(ChildDict[str, Product, Root], x)
            )
        ),
    ]

    @model_validator(mode="after")
    def set_parent(self) -> Self:
        cast(ChildDict[str, Product, Root], self.products).parent = self
        return self

    @classmethod
    def from_file(cls, file: Path) -> Root:
        """
        Loads a Root configuration from a YAML file.
        """
        yaml = Yaml(typ="safe")
        with file.open() as f:
            data = yaml.load(f)
        return Root.model_validate(data)

    @classmethod
    def from_ksem_config(
        cls,
        config_path: Path,
        *,
        product_name: str,
        instrument_group_name: str,
        instrument_name: str,
        store_settings_in: SettingsLocation | None = "root",
        store_pitch_range_setting_in: SettingsLocation = "instrument",
    ) -> Root:
        config = cast(KsemConfig, json.loads(config_path.read_text()))

        settings = Settings.from_ksem_config(config)

        instrument = Instrument(keyswitches=make_keyswitches(config, settings))
        instrument_group = InstrumentGroup(instruments={instrument_name: instrument})
        product = Product(instrument_groups={instrument_group_name: instrument_group})
        root = Root(products={product_name: product})

        match store_settings_in:
            case "root":
                root.settings = settings
            case "product":
                product.settings = settings
            case "instrument_group":
                instrument_group.settings = settings
            case "instrument":
                instrument.settings = settings
            case None:
                pass

        # Move the pitch range setting to wherever the user requested (it's a special
        # case)
        pitch_range = settings.pitch_range
        root.settings.pitch_range = Settings.default_pitch_range()
        match store_pitch_range_setting_in:
            case "root":
                root.settings.pitch_range = pitch_range
            case "product":
                product.settings.pitch_range = pitch_range
            case "instrument_group":
                instrument_group.settings.pitch_range = pitch_range
            case "instrument":
                instrument.settings.pitch_range = pitch_range

        return root

    @classmethod
    def combine(cls, *roots: Root) -> Root:
        return Root.model_validate(
            reduce(
                lambda a, b: deep_join_trees(a, b),
                (cast(Tree[object, object], i.model_dump()) for i in roots),
            )
        )

    def to_yaml(
        self, compact_settings: bool = True, compact_keyswitch_values: bool = True
    ) -> str:
        data = yaml_load(self.model_dump())

        def _iter_settings() -> Generator[Any, None, None]:
            if "settings" in data:
                yield data["settings"]

            for product in data["products"].values():
                if "settings" in product:
                    yield product["settings"]

                for group in product["instrument_groups"].values():
                    if "settings" in group:
                        yield group["settings"]

                    for instrument in group["instruments"].values():
                        if "settings" in instrument:
                            yield instrument["settings"]

        def _set_flow_style(obj: Any) -> None:
            if hasattr(obj, "fa"):
                obj.fa.set_flow_style()

        if compact_settings:
            for settings in _iter_settings():
                if settings is None:
                    continue
                for field in list(settings["midi_controls"].values()) + list(
                    settings["custom_bank"].values()
                ):
                    _set_flow_style(field)

        if compact_keyswitch_values:
            # Set flow style for concise keyswitch fields
            for keyswitches in (
                cast(Any, instrument["keyswitches"])
                for product in data["products"].values()
                for group in product["instrument_groups"].values()
                for instrument in group["instruments"].values()
            ):
                keyswitches["mapping"].fa.set_flow_style()
                for value in keyswitches["values"]:
                    _set_flow_style(value)

        return yaml_dumps(data)

    def _get_keyswitch_amount_option(
        self, instrument: Instrument, instrument_name: str
    ) -> int:
        total_keyswitches = len(instrument.keyswitches.values)
        if total_keyswitches <= 16:
            return 1
        elif total_keyswitches <= 32:
            return 2
        elif total_keyswitches <= 64:
            return 2
        else:
            raise ValueError(
                f"Instrument {instrument_name} has more than 64 keyswitches "
                f"({total_keyswitches})"
            )

    def _make_ksem_config(
        self,
        *,
        product_name: str,
        group_name: str,
        instrument_name: str,
        instrument: Instrument,
    ):
        file = Path(product_name, group_name, f"{instrument_name}.json")
        settings = instrument.get_merged_settings()

        with Note.with_middle_c(settings.middle_c):
            ksem_config: KsemConfig = {
                "KSEM-Version": float(KSEM_VERSION),
                "ks": instrument.keyswitches.to_ksem_config(settings),
                "midiControls": settings.midi_controls.to_ksem_config(),
                "customBank": settings.custom_bank.to_ksem_config(),
                "keySwitchSettings": {
                    "keySwitchAmount": self._get_keyswitch_amount_option(
                        instrument, instrument_name
                    ),
                    "sendMainKey": int(settings.send_main_key),
                },
                "xyFade": settings.xy_pad.to_ksem_config(),
                "delaySettings": settings.delay.to_ksem_config(),
                "automationSettings": settings.automation.to_ksem_config(),
                "keySwitchManager": {
                    **settings.router.to_ksem_config(),
                    "mpeSupportButton": int(settings.mpe_support),
                },
                "piano": {
                    "showHidePiano": 1,
                    "pitchLow": settings.pitch_range.low.to_midi(),
                    "pitchHigh": settings.pitch_range.high.to_midi(),
                    "automationKey": settings.automation.automation_key.to_midi(),
                },
                "pad": settings.control_pad.to_ksem_config(),
                "comments": (
                    settings.comment_template.format(
                        product=product_name,
                        instrument_group=group_name,
                        instrument=instrument_name,
                    )
                    if settings.comment_template
                    else ""
                ),
            }

        return KsemConfigFile(file=file, data=ksem_config)

    def write_ksem_config_files(self, root_dir: Path) -> None:
        """
        Writes KSEM configuration files to the specified root directory.
        """
        for config in self.to_ksem_configs():
            file = root_dir / config.file
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(json.dumps(config.data, indent=2))

    def to_ksem_configs(self) -> list[KsemConfigFile]:
        """
        Converts the Root configuration to a list of KsemConfigFile instances.
        """
        out: list[KsemConfigFile] = []

        for product_name, product in self.products.items():
            for group_name, group in product.instrument_groups.items():
                for instrument_name, instrument in group.instruments.items():
                    out.append(
                        self._make_ksem_config(
                            product_name=product_name,
                            group_name=group_name,
                            instrument_name=instrument_name,
                            instrument=instrument,
                        )
                    )
        return out


if __name__ == "__main__":
    # Load the root configuration from a YAML file and write KSEM config files
    loaded = Root.from_file(
        Path(
            r"H:\Libraries\Documents\_code\audio\ksem-transpiler\ksem_transpiler\example.yaml"
        )
    )
    print(
        loaded.write_ksem_config_files(
            Path(r"H:\Libraries\Documents\_code\audio\ksem-transpiler\output")
        )
    )
