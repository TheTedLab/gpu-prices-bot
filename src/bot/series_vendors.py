from src.bot.constants import *

series_dict = {
    0: "",
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: "GEFORCE GT 710",
    9: "GEFORCE GT 730",
    10: "GEFORCE 210",
    11: "GEFORCE GTX 1080 TI",
    12: "GEFORCE GTX 1050 TI",
    13: "GEFORCE GT 1030",
    14: "",
    15: "",
    16: "GEFORCE GTX 1660",
    17: "GEFORCE GTX 1660 TI",
    18: "GEFORCE GTX 1660 SUPER",
    19: "GEFORCE GTX 1650",
    20: "GEFORCE GTX 1650 SUPER",
    21: "GEFORCE GTX 1630",
    22: "",
    23: "",
    24: "GEFORCE RTX 2060",
    25: "GEFORCE RTX 2060 SUPER",
    26: "GEFORCE RTX 2080 TI",
    27: "GEFORCE RTX 2080 SUPER",
    28: "GEFORCE RTX 3050",
    29: "",
    30: "",
    31: "",
    32: "",
    33: "GEFORCE RTX 3060",
    34: "GEFORCE RTX 3060 TI",
    35: "GEFORCE RTX 3070",
    36: "GEFORCE RTX 3070 TI",
    37: "GEFORCE RTX 3080",
    38: "GEFORCE RTX 3080 TI",
    39: "GEFORCE RTX 3090",
    40: "GEFORCE RTX 3090 TI",
    41: "GEFORCE RTX 4080",
    42: "GEFORCE RTX 4090",
    43: "",
    44: "",
    45: "",
    46: "",
    47: "RADEON RX 550",
    48: "RADEON RX 560",
    49: "RADEON RX 580",
    50: "RADEON RX 5700 XT",
    51: "RADEON R7 240",
    52: "RADEON R9 370",
    53: "RADEON RX 6400",
    54: "RADEON RX 6500 XT",
    55: "",
    56: "",
    57: "",
    58: "",
    59: "RADEON RX 6600",
    60: "RADEON RX 6600 XT",
    61: "RADEON RX 6650 XT",
    62: "RADEON RX 6700",
    63: "RADEON RX 6700 XT",
    64: "RADEON RX 6750 XT",
    65: "RADEON RX 6800",
    66: "RADEON RX 6800 XT",
    67: "RADEON RX 6900",
    68: "RADEON RX 6900 XT",
    69: "RADEON RX 6950 XT",
    70: "QUADRO P2000",
    71: "QUADRO T400",
    72: "QUADRO RTX 6000",
    73: "",
    74: "QUADRO RTX A2000",
    75: "QUADRO RTX A4500",
    76: "TESLA GEFORCE A10",
    77: "TESLA A2",
    78: "TESLA T4",
    79: "QUADRO RTX A5000",
    80: "ARC A310",
    81: "ARC A380",
    82: "MATROX M9120",
}

vendors_dict = {
    0: "AFOX",
    1: "ASROCK",
    2: "ASUS",
    3: "BIOSTAR",
    4: "COLORFUL",
    5: "DELL",
    6: "EVGA",
    7: "GIGABYTE",
    8: "INNO3D",
    9: "KFA2",
    10: "MATROX",
    11: "MSI",
    12: "NVIDIA",
    13: "PALIT",
    14: "PNY",
    15: "POWERCOLOR",
    16: "SAPPHIRE",
    17: "SINOTEX",
    18: "XFX",
    19: "ZOTAC",
    20: "",
}

shops_dict = {
    0: "DNS",
    1: "MVIDEO",
    2: "CITILINK",
}

series_buttons_dict = {
    0: {
        "keyboard": keyboard_NVIDIA_10XX_SERIES,
        "returning": NVIDIA_10XX_SERIES_SUBMENU,
        "name": "NVIDIA 10XX SERIES"
    },
    1: {
        "keyboard": keyboard_NVIDIA_16XX_SERIES,
        "returning": NVIDIA_16XX_SERIES_SUBMENU,
        "name": "NVIDIA 16XX SERIES"
    },
    2: {
        "keyboard": keyboard_NVIDIA_20XX_SERIES,
        "returning": NVIDIA_20XX_SERIES_SUBMENU,
        "name": "NVIDIA 20XX SERIES"
    },
    3: {
        "keyboard": keyboard_NVIDIA_30XX_SERIES,
        "returning": NVIDIA_30XX_SERIES_SUBMENU,
        "name": "NVIDIA 30XX SERIES"
    },
    4: {
        "keyboard": keyboard_NVIDIA_40XX_SERIES,
        "returning": NVIDIA_40XX_SERIES_SUBMENU,
        "name": "NVIDIA 40XX SERIES"
    },
    5: {
        "keyboard": keyboard_NVIDIA_OTHER_SERIES,
        "returning": NVIDIA_OTHER_SUBMENU,
        "name": "NVIDIA OTHER SERIES"
    },
    6: {
        "keyboard": keyboard_NVIDIA_QUADRO_SERIES,
        "returning": NVIDIA_QUADRO_SERIES_SUBMENU,
        "name": "NVIDIA QUADRO SERIES"
    },
    7: {
        "keyboard": keyboard_NVIDIA_TESLA_SERIES,
        "returning": NVIDIA_TESLA_SERIES_SUBMENU,
        "name": "NVIDIA TESLA SERIES"
    },
    14: {
        "keyboard": keyboard_NVIDIA_1650X_SERIES,
        "returning": NVIDIA_1650X_SERIES_SUBMENU,
        "name": "NVIDIA 1650X SERIES"
    },
    15: {
        "keyboard": keyboard_NVIDIA_1660X_SERIES,
        "returning": NVIDIA_1660X_SERIES_SUBMENU,
        "name": "NVIDIA 1660X SERIES"
    },
    22: {
        "keyboard": keyboard_NVIDIA_2060X_SERIES,
        "returning": NVIDIA_2060X_SERIES_SUBMENU,
        "name": "NVIDIA 2060X SERIES"
    },
    23: {
        "keyboard": keyboard_NVIDIA_2080X_SERIES,
        "returning": NVIDIA_2080X_SERIES_SUBMENU,
        "name": "NVIDIA 2080X SERIES"
    },
    29: {
        "keyboard": keyboard_NVIDIA_3060X_SERIES,
        "returning": NVIDIA_3060X_SERIES_SUBMENU,
        "name": "NVIDIA 3060X SERIES"
    },
    30: {
        "keyboard": keyboard_NVIDIA_3070X_SERIES,
        "returning": NVIDIA_3070X_SERIES_SUBMENU,
        "name": "NVIDIA 3070X SERIES"
    },
    31: {
        "keyboard": keyboard_NVIDIA_3080X_SERIES,
        "returning": NVIDIA_3080X_SERIES_SUBMENU,
        "name": "NVIDIA 3080X SERIES"
    },
    32: {
        "keyboard": keyboard_NVIDIA_3090X_SERIES,
        "returning": NVIDIA_3090X_SERIES_SUBMENU,
        "name": "NVIDIA 3090X SERIES"
    },
    43: {
        "keyboard": keyboard_AMD_RX_5XX_SERIES,
        "returning": AMD_RX_5XX_SERIES_SUBMENU,
        "name": "AMD RX 5XX SERIES"
    },
    44: {
        "keyboard": keyboard_AMD_RX_5XXX_SERIES,
        "returning": AMD_RX_5XXX_SERIES_SUBMENU,
        "name": "AMD RX 5XXX SERIES"
    },
    45: {
        "keyboard": keyboard_AMD_RX_6XXX_SERIES,
        "returning": AMD_RX_6XXX_SERIES_SUBMENU,
        "name": "AMD RX 6XXX SERIES"
    },
    46: {
        "keyboard": keyboard_AMD_OTHER_SERIES,
        "returning": AMD_OTHER_SUBMENU,
        "name": "AMD OTHER SERIES"
    },
    55: {
        "keyboard": keyboard_AMD_RX_66XX_SERIES,
        "returning": AMD_RX_66XX_SERIES_SUBMENU,
        "name": "AMD RX 66XX SERIES"
    },
    56: {
        "keyboard": keyboard_AMD_RX_67XX_SERIES,
        "returning": AMD_RX_67XX_SERIES_SUBMENU,
        "name": "AMD RX 67XX SERIES"
    },
    57: {
        "keyboard": keyboard_AMD_RX_68XX_SERIES,
        "returning": AMD_RX_68XX_SERIES_SUBMENU,
        "name": "AMD RX 68XX SERIES"
    },
    58: {
        "keyboard": keyboard_AMD_RX_69XX_SERIES,
        "returning": AMD_RX_69XX_SERIES_SUBMENU,
        "name": "AMD RX 69XX SERIES"
    },
    73: {
        "keyboard": keyboard_NVIDIA_QUADRO_RTX_AXXXX_SERIES,
        "returning": NVIDIA_QUADRO_RTX_AXXXX_SERIES_SUBMENU,
        "name": "NVIDIA QUADRO RTX AXXXX SERIES"
    },
}
