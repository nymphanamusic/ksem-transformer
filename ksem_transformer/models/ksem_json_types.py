from __future__ import annotations

from typing import Literal, TypedDict

EMPTY_VALUE = "-"
type EmptyValue = Literal["-"]

KsemKeyswitchesEntry = TypedDict(
    "KsemKeyswitchesEntry",
    {
        "name": str | EmptyValue,
        "key": int | EmptyValue,
        "+key": int | EmptyValue,
        "bnk": int | EmptyValue,
        "sub": int | EmptyValue,
        "pgm": int | EmptyValue,
        "ccn": int | EmptyValue,
        "ccv": int | EmptyValue,
        "chn": int | EmptyValue,
        "color": list[int] | EmptyValue,
    },
)

KsemMidiControls = TypedDict(
    "KsemMidiControls",
    {
        "01Modulation_button": int,
        "01Modulation_dial": int,
        "02Breath_button": int,
        "02Breath_dial": int,
        "04FootPedal_button": int,
        "04FootPedal_dial": int,
        "05PortamentoTime_button": int,
        "05PortamentoTime_dial": int,
        "07Volume_button": int,
        "07Volume_dial": int,
        "10Pan_button": int,
        "10Pan_dial": int,
        "11Expression_button": int,
        "11Expression_dial": int,
        "64HoldPedal_button": int,
        "64HoldPedal_dial": int,
        "65PortamentoOnOff_button": int,
        "65PortamentoOnOff_dial": int,
        "66SostenutoPedal_button": int,
        "66SostenutoPedal_dial": int,
        "67SoftPedal_button": int,
        "67SoftPedal_dial": int,
        "68LegatoPedal_button": int,
        "68LegatoPedal_dial": int,
        "71Resonance_button": int,
        "71Resonance_dial": int,
        "74FrequencyCutoff_button": int,
        "74FrequencyCutoff_dial": int,
        "91ReverbLevel_button": int,
        "91ReverbLevel_dial": int,
        "93ChorusLevel_button": int,
        "93ChorusLevel_dial": int,
        "CcCustom01_button": int,
        "CcCustom01_num": int,
        "CcCustom01_dial": int,
        "CcCustom02_button": int,
        "CcCustom02_num": int,
        "CcCustom02_dial": int,
        "CcCustom03_button": int,
        "CcCustom03_num": int,
        "CcCustom03_dial": int,
        "CcCustom04_button": int,
        "CcCustom04_num": int,
        "CcCustom04_dial": int,
        "CcCustom05_button": int,
        "CcCustom05_num": int,
        "CcCustom05_dial": int,
        "CcCustom06_button": int,
        "CcCustom06_num": int,
        "CcCustom06_dial": int,
        "CcCustom07_button": int,
        "CcCustom07_num": int,
        "CcCustom07_dial": int,
        "CcCustom08_button": int,
        "CcCustom08_num": int,
        "CcCustom08_dial": int,
    },
)

KsemCustomBank = TypedDict(
    "KsemCustomBank",
    {
        "showHideCustomBank": int,
        "ctrl1_menu": int,
        "ctrl2_menu": int,
        "ctrl3_menu": int,
        "ctrl4_menu": int,
        "ctrl5_menu": int,
        "ctrl6_menu": int,
        "ctrl7_menu": int,
        "ctrl8_menu": int,
        "label": "KsemCustomBankLabel",
    },
)

KsemCustomBankLabel = TypedDict(
    "KsemCustomBankLabel",
    {
        "ctrl1": str,
        "ctrl2": str,
        "ctrl3": str,
        "ctrl4": str,
        "ctrl5": str,
        "ctrl6": str,
        "ctrl7": str,
        "ctrl8": str,
    },
)

KsemKeyswitchSettings = TypedDict(
    "KsemKeyswitchSettings", {"keySwitchAmount": int, "sendMainKey": int}
)

KsemXYFade = TypedDict(
    "KsemXYFade",
    {"chooseXFade": int, "chooseYFade": int, "xyFadeShape": int, "yOrientation": int},
)

KsemDelaySettings = TypedDict(
    "KsemDelaySettings",
    {
        "usageRack": float,
        "filterMIDICtrl": float,
        "bufferSize": float,
        "delayCompensation": float,
        "lock": float,
        "delayBank": float,
        "delaySub": float,
        "delayPgm": float,
        "delayCC": float,
        "delayMainKey": float,
        "delayAdditionalKey": float,
        "delayMIDINote": float,
    },
)

KsemAutomationSettings = TypedDict(
    "KsemAutomationSettings",
    {
        "automationKeySetting": int,
        "ignoreRepeatedKey": int,
        "autoTrigger": int,
        "protectAutomation": int,
    },
)

KsemKeySwitchManager = TypedDict(
    "KsemKeySwitchManager",
    {"routerTrack": int, "routerFilter": int, "mpeSupportButton": int},
)

KsemPiano = TypedDict(
    "KsemPiano",
    {"showHidePiano": int, "pitchLow": int, "pitchHigh": int, "automationKey": int},
)

KsemPad = TypedDict(
    "KsemPad",
    {
        "fontSize": list[int],
        "justification": int,
        "showKSNumbers": int,
        "showKSNotes": int,
        "fontSizeButton": int,
    },
)

KsemConfig = TypedDict(
    "KsemConfig",
    {
        "KSEM-Version": float,
        "ks": dict[str, KsemKeyswitchesEntry],
        "midiControls": KsemMidiControls,
        "customBank": KsemCustomBank,
        "keySwitchSettings": KsemKeyswitchSettings,
        "xyFade": KsemXYFade,
        "delaySettings": KsemDelaySettings,
        "automationSettings": KsemAutomationSettings,
        "keySwitchManager": KsemKeySwitchManager,
        "piano": KsemPiano,
        "pad": KsemPad,
        "comments": str,
    },
)
