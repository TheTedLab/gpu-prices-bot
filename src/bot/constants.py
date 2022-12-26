from telegram import InlineKeyboardButton

# UTF-8 коды для эмодзи
hand_emoji = u'\U0001F44B'
check_mark = u'\U00002705'
cross_mark = u'\U0000274C'
right_triangle = u'\U000025B6'
memo_emoji = u'\U0001F4DD'
loudspeaker = u'\U0001F4E2'

# Состояния
MENU, STATS_SUBMENU, POPULARITY_SUBMENU, SHOPS_SUBMENU, VENDORS_SUBMENU, GPU_SUBMENU, \
    POPULARITY_SHOPS_SUBMENU, POPULARITY_VENDORS_SUBMENU, \
    POPULARITY_SHOPS_GRAPH_SUBMENU, POPULARITY_VENDORS_GRAPH_SUBMENU, \
    ARCHITECTURE_SUBMENU, NVIDIA_SERIES_SUBMENU, AMD_SERIES_SUBMENU, OTHER_ARCH_SUBMENU, \
    GRAPH_SUBMENU, INTEL_SERIES_SUBMENU, MATROX_SERIES_SUBMENU, \
    NVIDIA_OTHER_SUBMENU, AMD_OTHER_SUBMENU, NVIDIA_QUADRO_SERIES_SUBMENU, \
    NVIDIA_QUADRO_RTX_AXXXX_SERIES_SUBMENU, NVIDIA_TESLA_SERIES_SUBMENU, \
    NVIDIA_10XX_SERIES_SUBMENU, NVIDIA_16XX_SERIES_SUBMENU, NVIDIA_1660X_SERIES_SUBMENU, \
    NVIDIA_1650X_SERIES_SUBMENU, NVIDIA_20XX_SERIES_SUBMENU, NVIDIA_2060X_SERIES_SUBMENU, \
    NVIDIA_2080X_SERIES_SUBMENU, NVIDIA_30XX_SERIES_SUBMENU, NVIDIA_3060X_SERIES_SUBMENU, \
    NVIDIA_3070X_SERIES_SUBMENU, NVIDIA_3080X_SERIES_SUBMENU, NVIDIA_3090X_SERIES_SUBMENU, \
    NVIDIA_40XX_SERIES_SUBMENU, AMD_RX_5XX_SERIES_SUBMENU, AMD_RX_5XXX_SERIES_SUBMENU, \
    AMD_RX_6XXX_SERIES_SUBMENU, AMD_RX_66XX_SERIES_SUBMENU, AMD_RX_67XX_SERIES_SUBMENU, \
    AMD_RX_68XX_SERIES_SUBMENU, AMD_RX_69XX_SERIES_SUBMENU = range(42)
# Переходы
STATS, POPULARITY, FOR_SHOP, FOR_VENDOR, FOR_GPU,\
    POPULARITY_FOR_SHOP, POPULARITY_FOR_VENDOR, \
    CURRENT_SHOP, CURRENT_VENDOR, CURRENT_GPU, CURRENT_SUBMENU, CURRENT_ARCH, \
    CURRENT_GRAPH_LEVEL, CURRENT_GRAPH_DAYS, CURRENT_GRAPH_STATE, CURRENT_GRAPH_START, \
    CURRENT_GRAPH_GPU_LEVEL, CURRENT_GRAPH_GPU_DAYS, CURRENT_GRAPH_GPU_STATE, CURRENT_GRAPH_GPU_START, \
    CURRENT_GAME_SUBMENU, ON_GPU, ON_GPU_QUESTION, CURRENT_DATA, CURRENT_SERIES, GRAPH_SUBMENU_ON_GPU, \
    YES_ON_GPU, NO_ON_GPU, ON_SEARCH, SEARCH = range(30)
# Варианты ответа для SHOPS
DNS_SHOP, MVIDEO_SHOP, CITILINK_SHOP = range(3)
# Варианты ответа для ARCHITECTURES
NVIDIA, AMD, OTHER_ARCH, INTEL, MATROX = range(5)
# Варианты ответа для SERIES
NVIDIA_10XX_SERIES, NVIDIA_16XX_SERIES, NVIDIA_20XX_SERIES, NVIDIA_30XX_SERIES, \
    NVIDIA_40XX_SERIES, NVIDIA_OTHER_SERIES, NVIDIA_QUADRO_SERIES, NVIDIA_TESLA_SERIES, \
    NVIDIA_GT_710_SERIES, NVIDIA_GT_730_SERIES, NVIDIA_210_SERIES, NVIDIA_1080_TI_SERIES, \
    NVIDIA_1050_TI_SERIES, NVIDIA_1030_SERIES, NVIDIA_1650X_SERIES, NVIDIA_1660X_SERIES, \
    NVIDIA_1660_SERIES, NVIDIA_1660_TI_SERIES, NVIDIA_1660_SUPER_SERIES, NVIDIA_1650_SERIES, \
    NVIDIA_1650_SUPER_SERIES, NVIDIA_1630_SERIES, NVIDIA_2060X_SERIES, NVIDIA_2080X_SERIES, \
    NVIDIA_2060_SERIES, NVIDIA_2060_SUPER_SERIES, NVIDIA_2080_TI_SERIES, NVIDIA_2080_SUPER_SERIES, \
    NVIDIA_3050_SERIES, NVIDIA_3060X_SERIES, NVIDIA_3070X_SERIES, NVIDIA_3080X_SERIES, \
    NVIDIA_3090X_SERIES, NVIDIA_3060_SERIES, NVIDIA_3060_TI_SERIES, NVIDIA_3070_SERIES, \
    NVIDIA_3070_TI_SERIES, NVIDIA_3080_SERIES, NVIDIA_3080_TI_SERIES, NVIDIA_3090_SERIES, \
    NVIDIA_3090_TI_SERIES, NVIDIA_4080_SERIES, NVIDIA_4090_SERIES, \
    AMD_RX5XX_SERIES, AMD_RX5XXX_SERIES, AMD_RX6XXX_SERIES, AMD_OTHER_SERIES, \
    AMD_RX_550_SERIES, AMD_RX_560_SERIES, AMD_RX_580_SERIES, AMD_RX_5700_XT_SERIES, \
    AMD_R7_240_SERIES, AMD_R9_370_SERIES, AMD_RX_6400_SERIES, AMD_RX_6500_XT_SERIES, \
    AMD_RX_66XX_SERIES, AMD_RX_67XX_SERIES, AMD_RX_68XX_SERIES, AMD_RX_69XX_SERIES, \
    AMD_RX_6600_SERIES, AMD_RX_6600_XT_SERIES, AMD_RX_6650_XT_SERIES, AMD_RX_6700_SERIES, \
    AMD_RX_6700_XT_SERIES, AMD_RX_6750_XT_SERIES, AMD_RX_6800_SERIES, AMD_RX_6800_XT_SERIES, \
    AMD_RX_6900_SERIES, AMD_RX_6900_XT_SERIES, AMD_RX_6950_XT_SERIES, \
    NVIDIA_QUADRO_P2000_SERIES, NVIDIA_QUADRO_T400_SERIES, NVIDIA_QUADRO_RTX_6000_SERIES, \
    NVIDIA_QUADRO_RTX_AXXXX_SERIES, NVIDIA_QUADRO_RTX_A2000_SERIES, NVIDIA_QUADRO_RTX_A4500_SERIES, \
    NVIDIA_TESLA_A10_SERIES, NVIDIA_TESLA_A2_SERIES, NVIDIA_TESLA_T4_SERIES, \
    NVIDIA_QUADRO_RTX_A5000_SERIES, ARC_A310_SERIES, ARC_A380_SERIES, MATROX_M9120_SERIES = range(83)
# Варианты ответа для VENDORS
VENDOR_AFOX, VENDOR_ASROCK, VENDOR_ASUS, VENDOR_BIOSTAR, VENDOR_COLORFUL, VENDOR_DELL, \
    VENDOR_EVGA, VENDOR_GIGABYTE, VENDOR_INNO3D, VENDOR_KFA2, VENDOR_MATROX, VENDOR_MSI, \
    VENDOR_NVIDIA, VENDOR_PALIT, VENDOR_PNY, VENDOR_POWERCOLOR, VENDOR_SAPPHIRE, VENDOR_SINOTEX, \
    VENDOR_XFX, VENDOR_ZOTAC = range(20)
# Варианты ответа для GRAPH
SHOW_30_DAYS, SHOW_60_DAYS, SHOW_90_DAYS, GRAPH_MIN, GRAPH_AVERAGE, GRAPH_MAX, BACK_TO_MENU = range(7)
# Варианты ответа для GRAPH_GPU
SHOW_30_DAYS_GPU, SHOW_60_DAYS_GPU, SHOW_90_DAYS_GPU, GRAPH_MIN_GPU, GRAPH_AVERAGE_GPU, \
    GRAPH_MAX_GPU = range(10, 16)

# Константные тексты
greetings_text = "Я информационный бот, который поможет тебе узнать цены " \
                 "на видеокарты в различных магазинах!"

using_buttons_text = "Чтобы получить информацию, воспользуйся кнопками:"
select_stats_text = "Выберите вид статистики:"
select_popularity_text = "Выберите вид популярности:"
select_shop_text = "Выберите магазин:"
select_vendor_text = "Выберите производителя:"
select_arch_text = "Выберите архитектуру видеокарты:"
select_series_text = "Выберите серию видеокарт:"
select_graph_text = "Выберите вид графика:"
select_gpu_text = "Напишите название интересующей вас видеокарты:"
help_text = "/start - начать разговор\n" \
            "/help - помощь\n" \
            "Чтобы получить информацию, просто напиши название игры\n" \
            "или воспользуйся кнопками меню!"

# Список текстов кнопок для поиска игр
gpu_search_list = []

# Клавиатуры кнопок
keyboard_MENU = [
    [InlineKeyboardButton("Статистика цен", callback_data=str(STATS))],
    [InlineKeyboardButton("Популярность видеокарт", callback_data=str(POPULARITY))],
]

keyboard_STATS = [
    [InlineKeyboardButton("По Магазину", callback_data=str(FOR_SHOP))],
    [InlineKeyboardButton("По Производителю", callback_data=str(FOR_VENDOR))],
    [InlineKeyboardButton("По Видеокарте", callback_data=str(FOR_GPU))],
]

keyboard_POPULARITY = [
    [InlineKeyboardButton("По Магазину", callback_data=str(POPULARITY_FOR_SHOP))],
    [InlineKeyboardButton("По Производителю", callback_data=str(POPULARITY_FOR_VENDOR))],
]

keyboard_ARCHITECTURES = [
    [
        InlineKeyboardButton("NVIDIA", callback_data=str(NVIDIA)),
        InlineKeyboardButton("AMD", callback_data=str(AMD)),
    ],
    [InlineKeyboardButton("Другие", callback_data=str(OTHER_ARCH))],
]

keyboard_OTHER_ARCH = [
    [
        InlineKeyboardButton("INTEL", callback_data=str(INTEL)),
        InlineKeyboardButton("MATROX", callback_data=str(MATROX)),
    ]
]

keyboard_NVIDIA_SERIES = [
    [
        InlineKeyboardButton("GeForce 10XX", callback_data=str(NVIDIA_10XX_SERIES)),
        InlineKeyboardButton("GeForce 16XX", callback_data=str(NVIDIA_16XX_SERIES)),
    ],
    [
        InlineKeyboardButton("GeForce 20XX", callback_data=str(NVIDIA_20XX_SERIES)),
        InlineKeyboardButton("GeForce 30XX", callback_data=str(NVIDIA_30XX_SERIES)),
    ],
    [
        InlineKeyboardButton("GeForce 40XX", callback_data=str(NVIDIA_40XX_SERIES)),
        InlineKeyboardButton("Другие", callback_data=str(NVIDIA_OTHER_SERIES)),
    ],
]

keyboard_NVIDIA_OTHER_SERIES = [
    [
        InlineKeyboardButton("Quadro", callback_data=str(NVIDIA_QUADRO_SERIES)),
        InlineKeyboardButton("Tesla", callback_data=str(NVIDIA_TESLA_SERIES)),
    ],
    [
        InlineKeyboardButton("GeForce GT 710", callback_data=str(NVIDIA_GT_710_SERIES)),
        InlineKeyboardButton("GeForce GT 730", callback_data=str(NVIDIA_GT_730_SERIES))
    ],
    [InlineKeyboardButton("GeForce 210", callback_data=str(NVIDIA_210_SERIES))],
]

keyboard_NVIDIA_QUADRO_SERIES = [
    [InlineKeyboardButton("Quadro P2000", callback_data=str(NVIDIA_QUADRO_P2000_SERIES))],
    [InlineKeyboardButton("Quadro T400", callback_data=str(NVIDIA_QUADRO_T400_SERIES))],
    [InlineKeyboardButton("Quadro RTX 6000", callback_data=str(NVIDIA_QUADRO_RTX_6000_SERIES))],
    [InlineKeyboardButton("Quadro RTX AXXXX", callback_data=str(NVIDIA_QUADRO_RTX_AXXXX_SERIES))],
]

keyboard_NVIDIA_QUADRO_RTX_AXXXX_SERIES = [
    [InlineKeyboardButton("Quadro RTX A2000", callback_data=str(NVIDIA_QUADRO_RTX_A2000_SERIES))],
    [InlineKeyboardButton("Quadro RTX A4500", callback_data=str(NVIDIA_QUADRO_RTX_A4500_SERIES))],
    [InlineKeyboardButton("Quadro RTX A5000", callback_data=str(NVIDIA_QUADRO_RTX_A5000_SERIES))],
]

keyboard_NVIDIA_TESLA_SERIES = [
    [InlineKeyboardButton("Tesla A10", callback_data=str(NVIDIA_TESLA_A10_SERIES))],
    [InlineKeyboardButton("Tesla A2", callback_data=str(NVIDIA_TESLA_A2_SERIES))],
    [InlineKeyboardButton("Tesla T4", callback_data=str(NVIDIA_TESLA_T4_SERIES))],
]

keyboard_NVIDIA_10XX_SERIES = [
    [InlineKeyboardButton("GeForce GTX 1080 TI", callback_data=str(NVIDIA_1080_TI_SERIES))],
    [InlineKeyboardButton("GeForce GTX 1050 TI", callback_data=str(NVIDIA_1050_TI_SERIES))],
    [InlineKeyboardButton("GeForce GT 1030", callback_data=str(NVIDIA_1030_SERIES))],
]

keyboard_NVIDIA_16XX_SERIES = [
    [InlineKeyboardButton("GeForce GTX 1630", callback_data=str(NVIDIA_1630_SERIES))],
    [InlineKeyboardButton("GeForce GTX 1650X", callback_data=str(NVIDIA_1650X_SERIES))],
    [InlineKeyboardButton("GeForce GTX 1660X", callback_data=str(NVIDIA_1660X_SERIES))],
]

keyboard_NVIDIA_1650X_SERIES = [
    [InlineKeyboardButton("GeForce GTX 1650", callback_data=str(NVIDIA_1650_SERIES))],
    [InlineKeyboardButton("GeForce GTX 1650 SUPER", callback_data=str(NVIDIA_1650_SUPER_SERIES))],
]

keyboard_NVIDIA_1660X_SERIES = [
    [InlineKeyboardButton("GeForce GTX 1660", callback_data=str(NVIDIA_1660_SERIES))],
    [InlineKeyboardButton("GeForce GTX 1660 TI", callback_data=str(NVIDIA_1660_TI_SERIES))],
    [InlineKeyboardButton("GeForce GTX 1660 SUPER", callback_data=str(NVIDIA_1660_SUPER_SERIES))],
]

keyboard_NVIDIA_20XX_SERIES = [
    [InlineKeyboardButton("GeForce RTX 2060X", callback_data=str(NVIDIA_2060X_SERIES))],
    [InlineKeyboardButton("GeForce RTX 2080X", callback_data=str(NVIDIA_2080X_SERIES))],
]

keyboard_NVIDIA_2060X_SERIES = [
    [InlineKeyboardButton("GeForce RTX 2060", callback_data=str(NVIDIA_2060_SERIES))],
    [InlineKeyboardButton("GeForce RTX 2060 SUPER", callback_data=str(NVIDIA_2060_SUPER_SERIES))],
]

keyboard_NVIDIA_2080X_SERIES = [
    [InlineKeyboardButton("GeForce RTX 2080 TI", callback_data=str(NVIDIA_2080_TI_SERIES))],
    [InlineKeyboardButton("GeForce RTX 2080 SUPER", callback_data=str(NVIDIA_2080_SUPER_SERIES))],
]

keyboard_NVIDIA_30XX_SERIES = [
    [InlineKeyboardButton("GeForce RTX 3050", callback_data=str(NVIDIA_3050_SERIES))],
    [InlineKeyboardButton("GeForce RTX 3060X", callback_data=str(NVIDIA_3060X_SERIES))],
    [InlineKeyboardButton("GeForce RTX 3070X", callback_data=str(NVIDIA_3070X_SERIES))],
    [InlineKeyboardButton("GeForce RTX 3080X", callback_data=str(NVIDIA_3080X_SERIES))],
    [InlineKeyboardButton("GeForce RTX 3090X", callback_data=str(NVIDIA_3090X_SERIES))],
]

keyboard_NVIDIA_3060X_SERIES = [
    [InlineKeyboardButton("GeForce RTX 3060", callback_data=str(NVIDIA_3060_SERIES))],
    [InlineKeyboardButton("GeForce RTX 3060 TI", callback_data=str(NVIDIA_3060_TI_SERIES))],
]

keyboard_NVIDIA_3070X_SERIES = [
    [InlineKeyboardButton("GeForce RTX 3070", callback_data=str(NVIDIA_3070_SERIES))],
    [InlineKeyboardButton("GeForce RTX 3070 TI", callback_data=str(NVIDIA_3070_TI_SERIES))],
]

keyboard_NVIDIA_3080X_SERIES = [
    [InlineKeyboardButton("GeForce RTX 3080", callback_data=str(NVIDIA_3080_SERIES))],
    [InlineKeyboardButton("GeForce RTX 3080 TI", callback_data=str(NVIDIA_3080_TI_SERIES))],
]

keyboard_NVIDIA_3090X_SERIES = [
    [InlineKeyboardButton("GeForce RTX 3090", callback_data=str(NVIDIA_3090_SERIES))],
    [InlineKeyboardButton("GeForce RTX 3090 TI", callback_data=str(NVIDIA_3090_TI_SERIES))],
]

keyboard_NVIDIA_40XX_SERIES = [
    [InlineKeyboardButton("GeForce RTX 4080", callback_data=str(NVIDIA_4080_SERIES))],
    [InlineKeyboardButton("GeForce RTX 4090", callback_data=str(NVIDIA_4090_SERIES))],
]

keyboard_AMD_SERIES = [
    [InlineKeyboardButton("Radeon RX 5XX", callback_data=str(AMD_RX5XX_SERIES))],
    [InlineKeyboardButton("Radeon RX 5XXX", callback_data=str(AMD_RX5XXX_SERIES))],
    [InlineKeyboardButton("Radeon RX 6XXX", callback_data=str(AMD_RX6XXX_SERIES))],
    [InlineKeyboardButton("Другие", callback_data=str(AMD_OTHER_SERIES))],
]

keyboard_AMD_OTHER_SERIES = [
    [InlineKeyboardButton("Radeon R7 240", callback_data=str(AMD_R7_240_SERIES))],
    [InlineKeyboardButton("Radeon R9 370", callback_data=str(AMD_R9_370_SERIES))],
]

keyboard_AMD_RX_5XX_SERIES = [
    [InlineKeyboardButton("Radeon RX 550", callback_data=str(AMD_RX_550_SERIES))],
    [InlineKeyboardButton("Radeon RX 560", callback_data=str(AMD_RX_560_SERIES))],
    [InlineKeyboardButton("Radeon RX 580", callback_data=str(AMD_RX_580_SERIES))],
]

keyboard_AMD_RX_5XXX_SERIES = [
    [InlineKeyboardButton("Radeon RX 5700 XT", callback_data=str(AMD_RX_5700_XT_SERIES))],
]

keyboard_AMD_RX_6XXX_SERIES = [
    [InlineKeyboardButton("Radeon RX 6400", callback_data=str(AMD_RX_6400_SERIES))],
    [InlineKeyboardButton("Radeon RX 6500 XT", callback_data=str(AMD_RX_6500_XT_SERIES))],
    [InlineKeyboardButton("Radeon RX 66XX", callback_data=str(AMD_RX_66XX_SERIES))],
    [InlineKeyboardButton("Radeon RX 67XX", callback_data=str(AMD_RX_67XX_SERIES))],
    [InlineKeyboardButton("Radeon RX 68XX", callback_data=str(AMD_RX_68XX_SERIES))],
    [InlineKeyboardButton("Radeon RX 69XX", callback_data=str(AMD_RX_69XX_SERIES))],
]

keyboard_AMD_RX_66XX_SERIES = [
    [InlineKeyboardButton("Radeon RX 6600", callback_data=str(AMD_RX_6600_SERIES))],
    [InlineKeyboardButton("Radeon RX 6600 XT", callback_data=str(AMD_RX_6600_XT_SERIES))],
    [InlineKeyboardButton("Radeon RX 6650 XT", callback_data=str(AMD_RX_6650_XT_SERIES))],
]

keyboard_AMD_RX_67XX_SERIES = [
    [InlineKeyboardButton("Radeon RX 6700", callback_data=str(AMD_RX_6700_SERIES))],
    [InlineKeyboardButton("Radeon RX 6700 XT", callback_data=str(AMD_RX_6700_XT_SERIES))],
    [InlineKeyboardButton("Radeon RX 6750 XT", callback_data=str(AMD_RX_6750_XT_SERIES))],
]

keyboard_AMD_RX_68XX_SERIES = [
    [InlineKeyboardButton("Radeon RX 6800", callback_data=str(AMD_RX_6800_SERIES))],
    [InlineKeyboardButton("Radeon RX 6800 XT", callback_data=str(AMD_RX_6800_XT_SERIES))],
]

keyboard_AMD_RX_69XX_SERIES = [
    [InlineKeyboardButton("Radeon RX 6900", callback_data=str(AMD_RX_6900_SERIES))],
    [InlineKeyboardButton("Radeon RX 6900 XT", callback_data=str(AMD_RX_6900_XT_SERIES))],
    [InlineKeyboardButton("Radeon RX 6950 XT", callback_data=str(AMD_RX_6950_XT_SERIES))],
]

keyboard_INTEL_SERIES = [
    [
        InlineKeyboardButton("Arc A310", callback_data=str(ARC_A310_SERIES)),
        InlineKeyboardButton("Arc A380", callback_data=str(ARC_A380_SERIES)),
    ],
]

keyboard_MATROX_SERIES = [
    [InlineKeyboardButton("Matrox M9120", callback_data=str(MATROX_M9120_SERIES))],
]

keyboard_GRAPH = [
    [
        InlineKeyboardButton("Мин", callback_data=str(GRAPH_MIN)),
        InlineKeyboardButton("Среднее", callback_data=str(GRAPH_AVERAGE)),
        InlineKeyboardButton("Макс", callback_data=str(GRAPH_MAX)),
    ],
    [
        InlineKeyboardButton("30 дней", callback_data=str(SHOW_30_DAYS)),
        InlineKeyboardButton("60 дней", callback_data=str(SHOW_60_DAYS)),
        InlineKeyboardButton("90 дней", callback_data=str(SHOW_90_DAYS)),
    ],
    [InlineKeyboardButton("Назад в меню", callback_data=str(BACK_TO_MENU))],
]

keyboard_GRAPH_GPU = [
    [
        InlineKeyboardButton("Мин", callback_data=str(GRAPH_MIN_GPU)),
        InlineKeyboardButton("Среднее", callback_data=str(GRAPH_AVERAGE_GPU)),
        InlineKeyboardButton("Макс", callback_data=str(GRAPH_MAX_GPU)),
    ],
    [
        InlineKeyboardButton("30 дней", callback_data=str(SHOW_30_DAYS_GPU)),
        InlineKeyboardButton("60 дней", callback_data=str(SHOW_60_DAYS_GPU)),
        InlineKeyboardButton("90 дней", callback_data=str(SHOW_90_DAYS_GPU)),
    ],
    [InlineKeyboardButton("Назад в меню", callback_data=str(BACK_TO_MENU))],
]

keyboard_VENDORS = [
    [
        InlineKeyboardButton("AFOX", callback_data=str(VENDOR_AFOX)),
        InlineKeyboardButton("ASRock", callback_data=str(VENDOR_ASROCK))
    ],
    [
        InlineKeyboardButton("ASUS", callback_data=str(VENDOR_ASUS)),
        InlineKeyboardButton("Biostar", callback_data=str(VENDOR_BIOSTAR))
    ],
    [
        InlineKeyboardButton("ColorFul", callback_data=str(VENDOR_COLORFUL)),
        InlineKeyboardButton("Dell", callback_data=str(VENDOR_DELL))
    ],
    [
        InlineKeyboardButton("EVGA", callback_data=str(VENDOR_EVGA)),
        InlineKeyboardButton("GIGABYTE", callback_data=str(VENDOR_GIGABYTE))
    ],
    [
        InlineKeyboardButton("inno3D", callback_data=str(VENDOR_INNO3D)),
        InlineKeyboardButton("KFA2", callback_data=str(VENDOR_KFA2))
    ],
    [
        InlineKeyboardButton("MATROX", callback_data=str(VENDOR_MATROX)),
        InlineKeyboardButton("MSI", callback_data=str(VENDOR_MSI))
    ],
    [
        InlineKeyboardButton("NVIDIA", callback_data=str(VENDOR_NVIDIA)),
        InlineKeyboardButton("Palit", callback_data=str(VENDOR_PALIT))
    ],
    [
        InlineKeyboardButton("PNY", callback_data=str(VENDOR_PNY)),
        InlineKeyboardButton("PowerColor", callback_data=str(VENDOR_POWERCOLOR))
    ],
    [
        InlineKeyboardButton("Sapphire", callback_data=str(VENDOR_SAPPHIRE)),
        InlineKeyboardButton("Sinotex", callback_data=str(VENDOR_SINOTEX))
    ],
    [
        InlineKeyboardButton("XFX", callback_data=str(VENDOR_XFX)),
        InlineKeyboardButton("Zotac", callback_data=str(VENDOR_ZOTAC))
    ],
]

keyboard_SHOPS = [
    [
        InlineKeyboardButton("DNS", callback_data=str(DNS_SHOP)),
        InlineKeyboardButton("MVIDEO", callback_data=str(MVIDEO_SHOP)),
        InlineKeyboardButton("CITILINK", callback_data=str(CITILINK_SHOP)),
    ]
]

keyboard_ON_SEARCH = [
    [
    ]
]

keyboard_ON_GPU = [
    [
    ]
]

keyboard_ONLY_BACK = [
    [
        InlineKeyboardButton("Назад в Меню", callback_data=str(NO_ON_GPU))
    ]
]

keyboard_ON_GAME_QUESTION = [
    [
        InlineKeyboardButton("Да", callback_data=str(YES_ON_GPU)),
        InlineKeyboardButton("Нет", callback_data=str(NO_ON_GPU)),
    ]
]
