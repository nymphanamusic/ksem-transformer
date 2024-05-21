from __future__ import annotations

import json
from pathlib import Path

import attrs
import yaml
from pydantic import BaseModel, Field

from ksem_transpiler.models.keyswitches import Keyswitches
from ksem_transpiler.models.ksem_json_types import KsemConfig
from ksem_transpiler.models.settings import Settings
from ksem_transpiler.models.utils import combine_dicts

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
                    file = Path(product_name, group_name, f"{instrument_name}.json")
                    settings = Settings.model_validate(
                        combine_dicts(
                            self.settings.model_dump(),
                            product.settings.model_dump(),
                            group.settings.model_dump(),
                            instrument.settings.model_dump(),
                        )
                    )
                    if settings.midi_controls is None:
                        raise ValueError(
                            "`midi_controls` must exist on a `settings` object in the "
                            "hierarchy"
                        )
                    if settings.custom_bank is None:
                        raise ValueError(
                            "`custom_bank` must exist on a `settings` object in the "
                            "hierarchy"
                        )

                    ksem_config: KsemConfig = {
                        "KSEM-Version": float(KSEM_VERSION),
                        "ks": instrument.keyswitches.to_ksem_config(settings),
                        "midiControls": settings.midi_controls.to_ksem_config(),
                        "customBank": settings.custom_bank.to_ksem_config(),
                        "keySwitchSettings": {"keySwitchAmount": 1, "sendMainKey": 1},
                        "xyFade": {
                            "chooseXFade": 3,
                            "chooseYFade": 13,
                            "xyFadeShape": 0,
                            "yOrientation": 0,
                        },
                        "delaySettings": {
                            "usageRack": 0.0,
                            "filterMIDICtrl": 0.0,
                            "bufferSize": 3.0,
                            "delayCompensation": 0.0,
                            "lock": 1.0,
                            "delayBank": 0.0,
                            "delaySub": 0.1,
                            "delayPgm": 0.2,
                            "delayCC": 0.3,
                            "delayMainKey": 0.5,
                            "delayAdditionalKey": 0.6,
                            "delayMIDINote": 1.0,
                        },
                        "automationSettings": {
                            "automationKeySetting": 0,
                            "ignoreRepeatedKey": 1,
                            "autoTrigger": 0,
                            "protectAutomation": 0,
                        },
                        "keySwitchManager": {
                            "routerTrack": 1,
                            "routerFilter": 0,
                            "mpeSupportButton": 1,
                        },
                        "piano": {
                            "showHidePiano": 1,
                            "pitchLow": 55,
                            "pitchHigh": 106,
                            "automationKey": 108,
                        },
                        "pad": {
                            "fontSize": [0, 0, 1],
                            "justification": 0,
                            "showKSNumbers": 1,
                            "showKSNotes": 0,
                            "fontSizeButton": 0,
                        },
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

                    out.append(KsemConfigFile(file=file, data=ksem_config))
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
