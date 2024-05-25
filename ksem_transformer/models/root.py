from __future__ import annotations

import json
from pathlib import Path

import attrs
import yaml
from pydantic import BaseModel, ConfigDict, Field

from ksem_transformer.models.keyswitches import Keyswitches
from ksem_transformer.models.ksem_json_types import KsemConfig, KsemKeyswitchSettings
from ksem_transformer.models.settings.settings import Settings
from ksem_transformer.models.utils import combine_dicts
from ksem_transformer.note import Note

KSEM_VERSION = "4.2"


@attrs.define()
class KsemConfigFile:
    """
    Represents a KSEM configuration file with its path and data.
    """

    file: Path
    data: KsemConfig


class Instrument(BaseModel):
    """
    Represents an instrument.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    settings: Settings = Field(default_factory=Settings)
    keyswitches: Keyswitches


class InstrumentGroup(BaseModel):
    """
    Represents a group of instruments.
    """

    settings: Settings = Field(default_factory=Settings)
    instruments: dict[str, Instrument]


class Product(BaseModel):
    """
    Represents a product.
    """

    settings: Settings = Field(default_factory=Settings)
    instrument_groups: dict[str, InstrumentGroup]


class Root(BaseModel):
    """
    Represents the root configuration.
    """

    settings: Settings = Field(default_factory=Settings)
    products: dict[str, Product]

    @classmethod
    def from_file(cls, file: Path) -> Root:
        """
        Loads a Root configuration from a YAML file.
        """
        with file.open() as f:
            data = yaml.load(f, Loader=yaml.Loader)
        return Root.model_validate(data)

    def _make_keyswitch_settings(
        self, instrument: Instrument, instrument_name: str
    ) -> KsemKeyswitchSettings:
        total_keyswitches = len(instrument.keyswitches.values)
        if total_keyswitches <= 16:
            amount_option_index = 1
        elif total_keyswitches <= 32:
            amount_option_index = 2
        elif total_keyswitches <= 64:
            amount_option_index = 2
        else:
            raise ValueError(
                f"Instrument {instrument_name} has more than 64 keyswitches "
                f"({total_keyswitches})"
            )

        return {"keySwitchAmount": amount_option_index, "sendMainKey": 1}

    def _make_ksem_config(
        self,
        *,
        product_name: str,
        product: Product,
        group_name: str,
        group: InstrumentGroup,
        instrument_name: str,
        instrument: Instrument,
    ):
        file = Path(product_name, group_name, f"{instrument_name}.json")
        settings = Settings.model_validate(
            combine_dicts(
                self.settings.model_dump(),
                product.settings.model_dump(),
                group.settings.model_dump(),
                instrument.settings.model_dump(),
            )
        )

        with Note.with_middle_c(settings.middle_c):
            ksem_config: KsemConfig = {
                "KSEM-Version": float(KSEM_VERSION),
                "ks": instrument.keyswitches.to_ksem_config(settings),
                "midiControls": settings.midi_controls.to_ksem_config(),
                "customBank": settings.custom_bank.to_ksem_config(),
                "keySwitchSettings": self._make_keyswitch_settings(
                    instrument, instrument_name
                ),
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
                            product=product,
                            group_name=group_name,
                            group=group,
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
