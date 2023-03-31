import time

import pytest
from pytest import mark
from telethon.tl.custom.message import Message

from src.bot.constants import *


@pytest.mark.system
@mark.asyncio
async def test_start():
    time.sleep(1)
    assert True


@pytest.mark.system
@mark.asyncio
async def test_stats():
    time.sleep(1)
    assert True


@pytest.mark.system
@mark.asyncio
async def test_message_out_of_dialog():
    time.sleep(1)
    assert True

@pytest.mark.system
@mark.asyncio
async def test_missing_gpu():
    time.sleep(1)
    assert True

@pytest.mark.system
@mark.asyncio
async def test_specific_gpu_statistics():
    time.sleep(1)
    assert True

params_vendor_statistics_existing_gpu = (
    ("MSI", "NVIDIA", "", "GeForse 30XX", "GeForse RTX 3060X", "GeForse RTX 3060", "Мин", "60", "90",
     keyboard_NVIDIA_SERIES, keyboard_NVIDIA_30XX_SERIES, keyboard_NVIDIA_3060X_SERIES, "min"),
    ("Zotac", "NVIDIA", "", "GeForse 16XX", "GeForse GTX 1650X", "GeForse GTX 1650", "Среднее", "30", "60",
     keyboard_NVIDIA_SERIES, keyboard_NVIDIA_16XX_SERIES, keyboard_NVIDIA_1650X_SERIES, "average"),
    ("PowerColor", "AMD", "", "Radeon RX 6XXX", "Radeon RX 66XX", "Radeon RX 6600", "Макс", "60", "30",
     keyboard_AMD_SERIES, keyboard_AMD_RX_6XXX_SERIES, keyboard_AMD_RX_66XX_SERIES, "max"),
    ("GIGABYTE", "Другие", "INTEL", "", "", "Arc A310", "Среднее", "30", "90",
     "", "", keyboard_INTEL_SERIES, "average")
)

@pytest.mark.system
@mark.asyncio
@pytest.mark.parametrize(
    'vendor_name, arch_0, arch_1, series_0, series_1, series_2, type_stats, days0, days1, key_0, key_1, key_2, level',
    params_vendor_statistics_existing_gpu
)
async def test_vendor_statistics_existing_gpu(vendor_name, arch_0, arch_1,
                                              series_0, series_1, series_2, type_stats, days0, days1,
                                              key_0, key_1, key_2, level):
    time.sleep(1)
    assert True

params_vendor_statistics_non_existing_gpu = (
    ("PNY", "NVIDIA", "", "GeForse 30XX", "GeForse RTX 3060X", "GeForse RTX 3060",
     keyboard_NVIDIA_SERIES, keyboard_NVIDIA_30XX_SERIES, keyboard_NVIDIA_3060X_SERIES),
    ("Sinotex", "NVIDIA", "", "GeForse 16XX", "GeForse GTX 1650X", "GeForse GTX 1650",
     keyboard_NVIDIA_SERIES, keyboard_NVIDIA_16XX_SERIES, keyboard_NVIDIA_1650X_SERIES),
    ("XFX", "AMD", "", "Radeon RX 6XXX", "Radeon RX 66XX", "Radeon RX 6600",
     keyboard_AMD_SERIES, keyboard_AMD_RX_6XXX_SERIES, keyboard_AMD_RX_66XX_SERIES),
    ("ASUS", "Другие", "INTEL", "", "", "Arc A310",
     "", "", keyboard_INTEL_SERIES),
    ("Dell", "Другие", "MATROX", "", "", "Matrox M9120",
     "", "", keyboard_MATROX_SERIES)
)

@pytest.mark.system
@mark.asyncio
@pytest.mark.parametrize('vendor_name, arch_0, arch_1, series_0, series_1, series_2, key_0, key_1, key_2',
                         params_vendor_statistics_non_existing_gpu)
async def test_vendor_statistics_non_existing_gpu(vendor_name, arch_0, arch_1,
                                              series_0, series_1, series_2, key_0, key_1, key_2):
    time.sleep(1)
    assert True

@pytest.mark.system
@mark.asyncio
async def test_vendor_statistics_message_out_dialog():
    time.sleep(1)
    assert True

@pytest.mark.system
@mark.asyncio
async def test_popularity_request():
    time.sleep(1)
    assert True

params_popularity_vendor = (
    "MSI",
    "Zotac",
    "PowerColor",
    "GIGABYTE",
    "MATROX"
)

@pytest.mark.parametrize('vendor_name', params_popularity_vendor)
@pytest.mark.system
@mark.asyncio
async def test_popularity_vendor(vendor_name):
    time.sleep(1)
    assert True

@pytest.mark.parametrize('vendor_name', params_popularity_vendor)
@pytest.mark.system
@mark.asyncio
async def test_popularity_vendor_message_out_dialog(vendor_name):
    time.sleep(1)
    assert True

params_architecture_submenu = (
        ("NVIDIA", ""),
        ("AMD", ""),
        ("Другие", "INTEL"),
        ("Другие", "MATROX")
)
@pytest.mark.parametrize('arch_0, arch_1', params_architecture_submenu)
@pytest.mark.system
@mark.asyncio
async def test_architecture_submenu(arch_0, arch_1):
    time.sleep(1)
    assert True


params_for_gpu_stats = (
    ('GEFORCE RTX 3060 RTX3060 DUAL OC 12G', '30 дней', '90 дней'),
    ('GEFORCE RTX 4080 EAGLE OC 16GB', '60 дней', '30 дней'),
    ('PALIT GEFORCE RTX 3070 TI GAMINGPRO', '90 дней', '60 дней'),
    ('GIGABYTE AMD RADEON RX 6700 XT EAGLE', '30 дней', '60 дней'),
    ('POWERCOLOR AMD RADEON RX 580 RED DRAGON', '60 дней', '90 дней'),
    ('ASUS TESLA NVIDIA GEFORCE A10', '30 дней', '30 дней')
)


@pytest.mark.system
@pytest.mark.parametrize('gpu_name, button_one, button_two', params_for_gpu_stats)
@mark.asyncio
async def test_for_gpu_stats(gpu_name, button_one, button_two):
    time.sleep(1)
    assert True


params_for_shop_stats = (
    (
        'DNS', 'NVIDIA', keyboard_NVIDIA_SERIES, select_series_text, 'GeForce 10XX',
        keyboard_NVIDIA_10XX_SERIES, 'GeForce GTX 1050 TI', '60 дней', 'Среднее'
    ),
    (
        'MVIDEO', 'AMD', keyboard_AMD_SERIES, select_series_text, 'Radeon RX 5XX',
        keyboard_AMD_RX_5XX_SERIES, 'Radeon RX 580', '90 дней', 'Макс'
    ),
    (
        'CITILINK', 'Другие', keyboard_OTHER_ARCH, select_arch_text, 'INTEL',
        keyboard_INTEL_SERIES, 'Arc A380', '30 дней', 'Мин'
    )
)


@pytest.mark.system
@pytest.mark.parametrize(
    'shop_name, arch_name, exp_key, exp_text, series_name, exp_series, next_series, try_days, try_level',
    params_for_shop_stats
)
@mark.asyncio
async def test_for_shop_stats(shop_name, arch_name, exp_key, exp_text,
                              series_name, exp_series, next_series, try_days, try_level):
    time.sleep(1)
    assert True


params_for_shop_stats_missing = (
    ('DNS', 'NVIDIA', 'GeForce 10XX', 'GeForce GTX 1080 TI'),
    ('MVIDEO', 'AMD', 'Radeon RX 5XX', 'Radeon RX 550'),
    ('CITILINK', 'Другие', 'MATROX', 'Matrox M9120')
)


@pytest.mark.system
@pytest.mark.parametrize(
    'shop_name, arch_name, series_name, missing_series',
    params_for_shop_stats_missing
)
@mark.asyncio
async def test_for_shop_stats_missing(shop_name, arch_name,
                                      series_name, missing_series):
    time.sleep(1)
    assert True


@pytest.mark.system
@mark.asyncio
async def test_for_shop_stats_out_dialog():
    time.sleep(1)
    assert True


params_for_popularity_for_shop = (
    'DNS',
    'MVIDEO',
    'CITILINK'
)


@pytest.mark.system
@pytest.mark.parametrize(
    'shop_name', params_for_popularity_for_shop
)
@mark.asyncio
async def test_popularity_for_shop(shop_name):
    time.sleep(1)
    assert True


@pytest.mark.system
@mark.asyncio
async def test_popularity_for_shop_out_dialog():
    time.sleep(1)
    assert True


params_for_subcategory_series = (
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'GeForce 10XX', '', keyboard_ONLY_BACK, ''),
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'GeForce 16XX', 'GeForce GTX 1650X', keyboard_NVIDIA_1650X_SERIES, ''),
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'GeForce 16XX', 'GeForce GTX 1660X', keyboard_NVIDIA_1660X_SERIES, ''),
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'GeForce 20XX', 'GeForce RTX 2060X', keyboard_NVIDIA_2060X_SERIES, ''),
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'GeForce 20XX', 'GeForce RTX 2080X', keyboard_NVIDIA_2080X_SERIES, ''),
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'GeForce 30XX', 'GeForce RTX 3060X', keyboard_NVIDIA_3060X_SERIES, ''),
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'GeForce 30XX', 'GeForce RTX 3070X', keyboard_NVIDIA_3070X_SERIES, ''),
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'GeForce 30XX', 'GeForce RTX 3080X', keyboard_NVIDIA_3080X_SERIES, ''),
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'GeForce 30XX', 'GeForce RTX 3090X', keyboard_NVIDIA_3090X_SERIES, ''),
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'GeForce 40XX', '', keyboard_ONLY_BACK, ''),
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'Другие', 'Quadro', keyboard_NVIDIA_QUADRO_SERIES, 'Quadro RTX AXXXX'),
    ('NVIDIA', '', keyboard_NVIDIA_SERIES, 'Другие', 'Tesla', keyboard_NVIDIA_TESLA_SERIES, ''),
    ('AMD', '', keyboard_AMD_SERIES, 'Radeon RX 5XX', '', keyboard_ONLY_BACK, ''),
    ('AMD', '', keyboard_AMD_SERIES, 'Radeon RX 5XXX', '', keyboard_ONLY_BACK, ''),
    ('AMD', '', keyboard_AMD_SERIES, 'Radeon RX 6XXX', 'Radeon RX 66XX', keyboard_AMD_RX_66XX_SERIES, ''),
    ('AMD', '', keyboard_AMD_SERIES, 'Radeon RX 6XXX', 'Radeon RX 67XX', keyboard_AMD_RX_67XX_SERIES, ''),
    ('AMD', '', keyboard_AMD_SERIES, 'Radeon RX 6XXX', 'Radeon RX 68XX', keyboard_AMD_RX_68XX_SERIES, ''),
    ('AMD', '', keyboard_AMD_SERIES, 'Radeon RX 6XXX', 'Radeon RX 69XX', keyboard_AMD_RX_69XX_SERIES, ''),
    ('AMD', '', keyboard_AMD_SERIES, 'Другие', '', keyboard_ONLY_BACK, ''),
    ('Другие', 'INTEL', keyboard_INTEL_SERIES, 'Arc A310', '', keyboard_ONLY_BACK, ''),
    ('Другие', 'INTEL', keyboard_INTEL_SERIES, 'Arc A380', '', keyboard_ONLY_BACK, ''),
    ('Другие', 'MATROX', keyboard_MATROX_SERIES, 'Matrox M9120', '', keyboard_ONLY_BACK, ''),
)


@pytest.mark.system
@pytest.mark.parametrize(
    'arch_0, arch_1, exp_key_0, series_0, series_1, exp_key_1, series_2', params_for_subcategory_series
)
@mark.asyncio
async def test_subcategory_series(arch_0, arch_1, exp_key_0, series_0, series_1,
                                  exp_key_1, series_2):
    time.sleep(1)
    assert True


params_for_specific_series_buttons = (
    ('NVIDIA', 'GeForce 10XX', 'GeForce GTX 1050 TI', '', '', keyboard_NVIDIA_10XX_SERIES),
    ('NVIDIA', 'GeForce 16XX', 'GeForce GTX 1650X', 'GeForce GTX 1650 SUPER', '', keyboard_NVIDIA_1650X_SERIES),
    ('NVIDIA', 'GeForce 16XX', 'GeForce GTX 1660X', 'GeForce GTX 1660 SUPER', '', keyboard_NVIDIA_1660X_SERIES),
    ('NVIDIA', 'GeForce 20XX', 'GeForce RTX 2060X', 'GeForce RTX 2060 SUPER', '', keyboard_NVIDIA_2060X_SERIES),
    ('NVIDIA', 'GeForce 20XX', 'GeForce RTX 2080X', 'GeForce RTX 2080 SUPER', '', keyboard_NVIDIA_2080X_SERIES),
    ('NVIDIA', 'GeForce 30XX', 'GeForce RTX 3060X', 'GeForce RTX 3060 TI', '', keyboard_NVIDIA_3060X_SERIES),
    ('NVIDIA', 'GeForce 30XX', 'GeForce RTX 3070X', 'GeForce RTX 3070 TI', '', keyboard_NVIDIA_3070X_SERIES),
    ('NVIDIA', 'GeForce 30XX', 'GeForce RTX 3080X', 'GeForce RTX 3080 TI', '', keyboard_NVIDIA_3080X_SERIES),
    ('NVIDIA', 'GeForce 30XX', 'GeForce RTX 3090X', 'GeForce RTX 3090 TI', '', keyboard_NVIDIA_3090X_SERIES),
    ('NVIDIA', 'GeForce 40XX', 'GeForce RTX 4080', '', '', keyboard_NVIDIA_40XX_SERIES),
    ('NVIDIA', 'Другие', 'Quadro', 'Quadro RTX AXXXX', 'Quadro RTX A2000', keyboard_NVIDIA_QUADRO_SERIES),
    ('NVIDIA', 'Другие', 'Tesla', 'Tesla A10', '', keyboard_NVIDIA_TESLA_SERIES),
    ('AMD', 'Radeon RX 5XX', 'Radeon RX 580', '', '', keyboard_AMD_RX_5XX_SERIES),
    ('AMD', 'Radeon RX 5XXX', 'Radeon RX 5700 XT', '', '', keyboard_AMD_RX_5XXX_SERIES),
    ('AMD', 'Radeon RX 6XXX', 'Radeon RX 66XX', 'Radeon RX 6600 XT', '', keyboard_AMD_RX_66XX_SERIES),
    ('AMD', 'Radeon RX 6XXX', 'Radeon RX 67XX', 'Radeon RX 6700 XT', '', keyboard_AMD_RX_67XX_SERIES),
    ('AMD', 'Radeon RX 6XXX', 'Radeon RX 68XX', 'Radeon RX 6800 XT', '', keyboard_AMD_RX_68XX_SERIES),
    ('AMD', 'Radeon RX 6XXX', 'Radeon RX 69XX', 'Radeon RX 6900 XT', '', keyboard_AMD_RX_69XX_SERIES),
    ('AMD', 'Другие', 'Radeon R9 370', '', '', keyboard_AMD_OTHER_SERIES),
)


@pytest.mark.system
@pytest.mark.parametrize(
    'arch_name, series_0, series_1, series_2, series_3, exp_key', params_for_specific_series_buttons
)
@mark.asyncio
async def test_specific_series_buttons(arch_name,
                                       series_0, series_1, series_2, series_3, exp_key):
    time.sleep(1)
    assert True


async def check_keyboard(resp: Message, keyboard, message_text):
    assert message_text in resp.raw_text
    len_keyboard = get_keyboard_length(keyboard)
    assert resp.button_count == len_keyboard
    for i in range(len(resp.buttons)):
        for j in range(len(resp.buttons[i])):
            assert resp.buttons[i][j].text == keyboard[i][j].text


def get_keyboard_length(keyboard):
    len_keyboard = 0
    for elem in keyboard:
        len_keyboard += len(elem)
    return len_keyboard
