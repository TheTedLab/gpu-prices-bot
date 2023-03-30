import time
import pytest
from pytest import mark
from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.custom.conversation import Conversation
from src.bot.constants import *


@pytest.mark.system
@mark.asyncio
async def test_start(client: TelegramClient):
    # Создание разговора с ботом
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # Отправка команды или любого сообщения
        # User > /start
        await conv.send_message("/start")

        # Получение ответа
        # Bot < Привет, {user}!
        resp: Message = await conv.get_response()
        assert "Привет" in resp.raw_text

        # Bot < Я информационный бот, который поможет тебе узнать цены
        # на видеокарты в различных магазинах!
        resp = await conv.get_response()
        assert greetings_text in resp.raw_text

        # Проверка клавиатуры
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)


@pytest.mark.system
@mark.asyncio
async def test_stats(client: TelegramClient):
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")

        # Bot < Привет, {user}!
        await conv.get_response()

        # Bot < Я информационный бот, который поможет тебе узнать цены
        # на видеокарты в различных магазинах!
        await conv.get_response()

        # Bot < Чтобы получить информацию, воспользуйся кнопками:
        # [Статистика цен][Популярность видеокарт]
        resp = await conv.get_response()
        # User > [Статистика цен]
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите вид статистики:
        # [По Магазину][По Производителю][По Видеокарте]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_STATS, select_stats_text)


@pytest.mark.system
@mark.asyncio
async def test_message_out_of_dialog(client: TelegramClient):
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")

        # Отправка сообщения вне диалога
        # User > redrum
        await conv.send_message("redrum")

        # Получение ответа
        # Bot < Ошибка! Необходимо выбрать кнопку.
        resp: Message = await conv.get_response()
        assert error_enter_text in resp.raw_text

@pytest.mark.system
@mark.asyncio
async def test_missing_gpu(client: TelegramClient):
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")
        resp: Message = await conv.get_response()

        # User p> Статистика цен
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите вид статистики: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_STATS, select_stats_text)

        # User p> По видеокарте
        await resp.click(text=keyboard_STATS[0][2].text)

        # Bot < Напишите название интересующей вас видеокарты:
        resp = await get_last_message(client, conv)
        assert select_gpu_text in resp.raw_text

        # User > Horsecard 3000
        await conv.send_message("Horsecard 3000")

        # Bot < Нет результатов поиска
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_ONLY_BACK, no_search_results_text)

        # User p> Назад в меню
        await resp.click(text=keyboard_ONLY_BACK[0][0].text)

        # Bot < НЧтобы получить информацию, воспользуйся кнопками: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)

@pytest.mark.system
@mark.asyncio
async def test_specific_gpu_statistics(client: TelegramClient):
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")
        resp: Message = await conv.get_response()

        # User p> Статистика цен
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите вид статистики: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_STATS, select_stats_text)

        # Отправка сообщения вне диалога
        # User > redrum
        await conv.send_message("redrum")

        # Bot < Ошибка! Необходимо выбрать кнопку.
        resp = await conv.get_response()
        assert error_enter_text in resp.raw_text

        # User p> По видеокарте
        await resp.click(text=keyboard_STATS[0][2].text)

        # Bot < Напишите название интересующей вас видеокарты:
        resp = await get_last_message(client, conv)
        assert select_gpu_text in resp.raw_text

        # User > Horsecard 3000
        await conv.send_message("Horsecard 3000")

        # Bot < Нет результатов поиска
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_ONLY_BACK, no_search_results_text)

        # User p> Назад в меню
        await resp.click(text=keyboard_ONLY_BACK[0][0].text)

        # Bot < Чтобы получить информацию, воспользуйся кнопками: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)

params_vendor_statistics_existing_gpu = (
    ("MSI", "NVIDIA", "", "GeForse 30XX", "GeForse RTX 3060X", "GeForse RTX 3060", "Мин", "60", "90",
     keyboard_NVIDIA_SERIES, keyboard_NVIDIA_30XX_SERIES, keyboard_NVIDIA_3060X_SERIES, "min"),
    ("Zotac", "NVIDIA", "", "GeForse 16XX", "GeForse GTX 1650X", "GeForse GTX 1650", "Среднее", "30", "60",
     keyboard_NVIDIA_SERIES, keyboard_NVIDIA_16XX_SERIES, keyboard_NVIDIA_1650X_SERIES, "average"),
    ("PowerColor", "AMD", "", "Radeon RX 6XXX", "Radeon RX 66XX", "Radeon RX 6600", "Макс", "60", "30",
     keyboard_AMD_SERIES, keyboard_AMD_RX_6XXX_SERIES, keyboard_AMD_RX_66XX_SERIES, "max"),
    ("GIGABYTE", "Другие", "INTEL", "", "", "Arc A310", "Среднее", "30", "90",
     "", "", keyboard_INTEL_SERIES, "average")
    # ("MATROX", "Другие", "MATROX", "", "", "Matrox M9120", "Мин", "90", "60",
    # "", "", keyboard_MATROX_SERIES, "min")
)

@pytest.mark.system
@mark.asyncio
@pytest.mark.parametrize('vendor_name, card_architecture_0, card_architecture_1, '
                         'card_series_0, card_series_1, card_series_2, '
                         'type_statistics, days0, days1,'
                         'key_0, key_1, key_2, level',
                         params_vendor_statistics_existing_gpu)
async def test_vendor_statistics_existing_gpu(client: TelegramClient, vendor_name,
                                              card_architecture_0, card_architecture_1,
                                              card_series_0, card_series_1, card_series_2,
                                              type_statistics, days0, days1,
                                              key_0, key_1, key_2, level):
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")
        resp: Message = await conv.get_response()

        # User p> Статистика цен
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите вид статистики: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_STATS, select_stats_text)

        # User p> По Производителю
        await resp.click(text=keyboard_STATS[0][1].text)

        # Bot < Выберите производителя + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_VENDORS, select_vendor_text)

        # User p> VendorName
        await resp.click(text=vendor_name)

        # Bot < Выберите архитектуру видеокарты: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_ARCHITECTURES, select_arch_text)

        # User p> CardArchitecture_0
        await resp.click(text=card_architecture_0)

        if card_architecture_1 != "":
            # Bot < Выберите архитектуру видеокарты: + кнопки
            resp = await get_last_message(client, conv)
            await check_keyboard(resp, keyboard_OTHER_ARCH, select_arch_text)

            # User p> CardArchitecture_1
            await resp.click(text=card_architecture_1)

        if card_series_0 != "":
            # Bot < Выберите архитектуру видеокарты: + кнопки
            resp = await get_last_message(client, conv)
            await check_keyboard(resp, key_0, select_series_text)

            # User p> CardSeries_0
            await resp.click(text=card_series_0)

        if card_series_1 != "":
            # Bot < Выберите архитектуру видеокарты: + кнопки
            resp = await get_last_message(client, conv)
            await check_keyboard(resp, key_1, select_series_text)

            # User p> CardSeries_1
            await resp.click(text=card_series_1)

        # Bot < Выберите архитектуру видеокарты: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, key_2, select_series_text)

        # User p> CardSeries_2
        await resp.click(text=card_series_2)

        # Bot < Выберите вид графика: + информация по карте и текущему графику + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_GRAPH, select_graph_text)

        assert "submenu: for_vendor" in resp.raw_text
        assert vendor_name.upper() in resp.raw_text
        if card_architecture_1 == 0:
            assert card_architecture_0.upper() in resp.raw_text
        else:
            assert card_architecture_1.upper() in resp.raw_text
        assert card_series_2.upper() in resp.raw_text
        assert "days: 30" in resp.raw_text
        assert "level: min" in resp.raw_text

        # User p> Days_0
        await resp.click(text=days0)
        # Bot < Обновлённая статистика
        assert "days: " + days0 in resp.raw_text

        # User p> Days_1
        await resp.click(text=days1)
        # Bot < Обновлённая статистика
        assert "days: " + days1 in resp.raw_text

        # User p> Level
        await resp.click(text=type_statistics)
        # Bot < Обновлённая статистика
        assert "level: " + level in resp.raw_text

        # User p> Назад в меню
        await resp.click(text=keyboard_GRAPH[2][0].text)

        # Bot < Чтобы получить информацию, воспользуйся кнопками: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)

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
@pytest.mark.parametrize('vendor_name, card_architecture_0, card_architecture_1,'
                         'card_series_0, card_series_1, card_series_2,'
                         'key_0, key_1, key_2',
                         params_vendor_statistics_non_existing_gpu)
async def test_vendor_statistics_non_existing_gpu(client: TelegramClient, vendor_name,
                                              card_architecture_0, card_architecture_1,
                                              card_series_0, card_series_1, card_series_2,
                                              key_0, key_1, key_2):
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")
        resp: Message = await conv.get_response()

        # User p> Статистика цен
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите вид статистики: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_STATS, select_stats_text)

        # User p> По Производителю
        await resp.click(text=keyboard_STATS[0][1].text)

        # Bot < Выберите производителя + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_VENDORS, select_vendor_text)

        # User p> VendorName
        await resp.click(text=vendor_name)

        # Bot < Выберите архитектуру видеокарты: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_ARCHITECTURES, select_arch_text)

        # User p> CardArchitecture_0
        await resp.click(text=card_architecture_0)

        if card_architecture_1 != "":
            # Bot < Выберите архитектуру видеокарты: + кнопки
            resp = await get_last_message(client, conv)
            await check_keyboard(resp, keyboard_OTHER_ARCH, select_arch_text)

            # User p> CardArchitecture_1
            await resp.click(text=card_architecture_1)

        if card_series_0 != "":
            # Bot < Выберите архитектуру видеокарты: + кнопки
            resp = await get_last_message(client, conv)
            await check_keyboard(resp, key_0, select_series_text)

            # User p> CardSeries_0
            await resp.click(text=card_series_0)

        if card_series_1 != "":
            # Bot < Выберите архитектуру видеокарты: + кнопки
            resp = await get_last_message(client, conv)
            await check_keyboard(resp, key_1, select_series_text)

            # User p> CardSeries_1
            await resp.click(text=card_series_1)

        # Bot < Выберите архитектуру видеокарты: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, key_2, select_series_text)

        # User p> CardSeries_2
        await resp.click(text=card_series_2)

        # Bot < Нет данных по выбранным параметрам
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_ONLY_BACK, no_data_text)

        # User p> Назад в меню
        await resp.click(text=keyboard_ONLY_BACK[0][0].text)

        # Bot < Чтобы получить информацию, воспользуйся кнопками: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)

@pytest.mark.system
@mark.asyncio
async def test_vendor_statistics_message_out_dialog(client: TelegramClient):
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")
        resp: Message = await conv.get_response()

        # User p> Статистика цен
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите вид статистики: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_STATS, select_stats_text)

        # User p> По Производителю
        await resp.click(text=keyboard_STATS[0][1].text)

        # Bot < Выберите производителя + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_VENDORS, select_vendor_text)

        # Отправка сообщения вне диалога
        # User > redrum
        await conv.send_message("redrum")

        # Bot < Ошибка! Необходимо выбрать кнопку.
        resp = await conv.get_response()
        assert error_enter_text in resp.raw_text

        # User p> Zotac
        await resp.click(text="Zotac")

        # Bot < Выберите архитектуру видеокарты: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_ARCHITECTURES, select_arch_text)

@pytest.mark.system
@mark.asyncio
async def test_popularity_request(client: TelegramClient):
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")
        resp: Message = await conv.get_response()

        # User p> Популярность видеокарт
        await resp.click(text=keyboard_MENU[0][1].text)

        # Bot < Выберите вид популярности: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_POPULARITY, select_popularity_text)

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
async def test_popularity_vendor(client: TelegramClient, vendor_name):
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")
        resp: Message = await conv.get_response()

        # User p> Популярность видеокарт
        await resp.click(text=keyboard_MENU[0][1].text)

        # Bot < Выберите вид популярности: + кнопки
        resp = await get_last_message(client, conv)

        # User p> По Производителю
        await resp.click(text=keyboard_POPULARITY[0][1].text)

        # Bot < Выберите производителя + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_VENDORS, select_vendor_text)

        # User p> VendorName
        await resp.click(text=vendor_name)

        # Bot < График + описание + кнопка Назад в меню
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_POPULARITY_GRAPH, popularity_vendor_text)
        assert vendor_name.upper() in resp.raw_text

        # User p> Назад в меню
        await resp.click(text=keyboard_POPULARITY_GRAPH[0][0].text)

        # Bot < Чтобы получить информацию, воспользуйся кнопками: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)

@pytest.mark.parametrize('vendor_name', params_popularity_vendor)
@pytest.mark.system
@mark.asyncio
async def test_popularity_vendor_message_out_dialog(client: TelegramClient, vendor_name):
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")
        resp: Message = await conv.get_response()

        # User p> Популярность видеокарт
        await resp.click(text=keyboard_MENU[0][1].text)

        # Bot < Выберите вид популярности: + кнопки
        resp = await get_last_message(client, conv)

        # User p> По Производителю
        await resp.click(text=keyboard_POPULARITY[0][1].text)

        # Bot < Выберите производителя + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_VENDORS, select_vendor_text)

        # Отправка сообщения вне диалога
        # User > redrum
        await conv.send_message("redrum")

        # Bot < Ошибка! Необходимо выбрать кнопку.
        resp = await conv.get_response()
        assert error_enter_text in resp.raw_text

        # User p> VendorName
        await resp.click(text=vendor_name)

        # Bot < График + описание + кнопка Назад в меню
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_POPULARITY_GRAPH, popularity_vendor_text)
        assert vendor_name.upper() in resp.raw_text

        # User p> Назад в меню
        await resp.click(text=keyboard_POPULARITY_GRAPH[0][0].text)

        # Bot < Чтобы получить информацию, воспользуйся кнопками: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)

params_architecture_submenu = (
        ("NVIDIA", ""),
        ("AMD", ""),
        ("Другие", "INTEL"),
        ("Другие", "MATROX")
)
@pytest.mark.parametrize('arch_0, arch_1', params_architecture_submenu)
@pytest.mark.system
@mark.asyncio
async def test_architecture_submenu(client: TelegramClient, arch_0, arch_1):
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # User > /start
        await conv.send_message("/start")
        resp: Message = await conv.get_response()

        # User p> Статистика цен
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите вид статистики: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_STATS, select_stats_text)

        # User p> По Производителю
        await resp.click(text=keyboard_STATS[0][1].text)

        # Bot < Выберите производителя + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_VENDORS, select_vendor_text)

        # User p> VendorName
        await resp.click(text="XFX")

        # Bot < Выберите архитектуру видеокарты: + кнопки
        resp = await get_last_message(client, conv)
        await check_keyboard(resp, keyboard_ARCHITECTURES, select_arch_text)

        # User p> CardArchitecture_0
        await resp.click(text=arch_0)

        if arch_1 != "":
            # Bot < Выберите архитектуру видеокарты: + кнопки
            resp = await get_last_message(client, conv)
            await check_keyboard(resp, keyboard_OTHER_ARCH, select_arch_text)

            # User p> CardArchitecture_1
            await resp.click(text=arch_1)


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
async def test_for_gpu_stats(client: TelegramClient, gpu_name, button_one, button_two):
    async with client.conversation('@GpuPricesBot', timeout=10) as conv:
        # User > /start
        await conv.send_message("/start")

        # Bot < Привет, {user}!
        await conv.get_response()

        # Bot < Я информационный бот, который поможет тебе узнать цены
        # на видеокарты в различных магазинах!
        await conv.get_response()

        # Bot < Чтобы получить информацию, воспользуйся кнопками:
        # [Статистика цен][Популярность видеокарт]
        resp = await conv.get_response()
        # User > [Статистика цен]
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите вид статистики:
        # [По Магазину][По Производителю][По Видеокарте]
        resp = await get_last_message(client, conv, timeout=5)
        # User > [По Видеокарте]
        await resp.click(text=keyboard_STATS[0][2].text)

        # Bot < Напишите название интересующей вас видеокарты:
        resp = await get_last_message(client, conv, timeout=5)
        assert select_gpu_text in resp.raw_text
        # User > gpu_name
        resp = await conv.send_message(gpu_name)

        # Bot < Результаты поиска для gpu_name:
        # [gpu_name]
        await check_keyboard(resp, keyboard_ON_SEARCH, search_results_for_text + gpu_name + ": ")
        # User > [gpu_name]
        await resp.click(text=keyboard_ON_SEARCH[0][0].text)

        # Bot < Выберите вид графика:
        # [30 дней][60 дней][90 дней]
        # [Назад в меню]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_GRAPH_PERIODS, select_graph_text)
        # User > [button_one]
        await resp.click(text=button_one)

        caption_message_text = f'submenu: for_gpu\n' \
                               f'gpu: {gpu_name}\n' \
                               f'days: {str(button_one.split(" ")[0])}\n' + select_graph_text

        # Bot < caption_message + Выберите вид графика:
        # [30 дней][60 дней][90 дней]
        # [Назад в меню]
        resp = await get_last_message(client, conv, timeout=10)
        await check_keyboard(resp, keyboard_GRAPH_PERIODS, caption_message_text)
        # User > [button_two]
        await resp.click(text=button_two)

        caption_message_text = f'submenu: for_gpu\n' \
                               f'gpu: {gpu_name}\n' \
                               f'days: {str(button_two.split(" ")[0])}\n' + select_graph_text

        # Bot < caption_message + Выберите вид графика:
        # [30 дней][60 дней][90 дней]
        # [Назад в меню]
        resp = await get_last_message(client, conv, timeout=10)
        await check_keyboard(resp, keyboard_GRAPH_PERIODS, caption_message_text)
        # User > [Назад в меню]
        await resp.click(text=keyboard_GRAPH_PERIODS[1][0].text)

        # Bot < Чтобы получить информацию, воспользуйся кнопками:
        # [Статистика цен][Популярность видеокарт]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)


params_for_shop_stats = (
    (
        'DNS', 'NVIDIA', keyboard_NVIDIA_SERIES, select_series_text, 'GeForce 10XX', 'GeForce GTX 1050 TI',
        '60 дней', 'Среднее'
    ),
    (
        'MVIDEO', 'AMD', keyboard_AMD_SERIES, select_series_text, 'Radeon RX 5XX', 'Radeon RX 580',
        '90 дней', 'Макс'
    ),
    (
        'CITILINK', 'Другие', keyboard_OTHER_ARCH, select_arch_text, 'INTEL', 'Arc A380',
        '30 дней', 'Мин'
    )
)


@pytest.mark.system
@pytest.mark.parametrize(
    'shop_name, arch_name, exp_key, exp_text, series_name, exp_series, next_series, try_days, try_level',
    params_for_shop_stats
)
@mark.asyncio
async def test_for_shop_stats(client: TelegramClient, shop_name, arch_name, exp_key, exp_text,
                              series_name, exp_series, next_series, try_days, try_level):
    async with client.conversation('@GpuPricesBot', timeout=10) as conv:
        # User > /start
        await conv.send_message("/start")

        # Bot < Привет, {user}!
        await conv.get_response()

        # Bot < Я информационный бот, который поможет тебе узнать цены
        # на видеокарты в различных магазинах!
        await conv.get_response()

        # Bot < Чтобы получить информацию, воспользуйся кнопками:
        # [Статистика цен][Популярность видеокарт]
        resp = await conv.get_response()
        # User > [Статистика цен]
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите вид статистики:
        # [По Магазину][По Производителю][По Видеокарте]
        resp = await get_last_message(client, conv, timeout=5)
        # User > [По Магазину]
        await resp.click(text=keyboard_STATS[0][0].text)

        # Bot < Выберите магазин:
        # [DNS][MVIDEO][CITILINK]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_GRAPH_PERIODS, select_graph_text)
        # User > [shop_name]
        await resp.click(text=shop_name)

        # Bot < Выберите архитектуру видеокарты:
        # [NVIDIA][AMD]
        # [Другие]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_ARCHITECTURES, select_arch_text)
        # User > [arch_name]
        await resp.click(text=arch_name)

        # Bot < Выберите серию видеокарт:
        # NVIDIA
        # [Geforce 10XX][Geforce 16XX]
        # [Geforce 20XX][Geforce 30XX]
        # [Geforce 40XX][Другие]
        # AMD
        # [Radeon RX 5XX][Radeon RX 5XXX]
        # [Radeon RX 6XXX][Другие]
        # Другие
        # [INTEL][MATROX]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, exp_key, exp_text)
        # User > [series_name]
        await resp.click(text=series_name)

        # Bot < Выберите серию видеокарт:
        # NVIDIA - Geforce 10XX
        # [GeForce GTX 1080 TI][GeForce GTX 1050 TI][GeForce GT 1030]
        # AMD - Radeon RX 5XX
        # [Radeon RX 550][Radeon RX 560][Radeon RX 580]
        # INTEL
        # [Arc A310][Arc A380]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, exp_series, select_series_text)
        # User > [next_series]
        await resp.click(text=next_series)

        caption_message_text = f'submenu: for_shop\n' \
                               f'shop: {shop_name}\n' \
                               f'vendor: \n' \
                               f'arch: {arch_name}\n' \
                               f'series: {next_series}\n' \
                               f'days: 30\n' \
                               f'level: min\n' + select_graph_text

        # Bot < caption_message + Выберите вид графика:
        # [Мин][Среднее][Макс]
        # [30 дней][60 дней][90 дней]
        # [Назад в меню]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_GRAPH, caption_message_text)
        # User > [try_days] = 30,60,90
        await resp.click(text=try_days)

        caption_message_text = f'submenu: for_shop\n' \
                               f'shop: {shop_name}\n' \
                               f'vendor: \n' \
                               f'arch: {arch_name}\n' \
                               f'series: {next_series}\n' \
                               f'days: {try_days.split(" ")[0]}\n' \
                               f'level: min\n' + select_graph_text

        # Bot < caption_message + Выберите вид графика:
        # [Мин][Среднее][Макс]
        # [30 дней][60 дней][90 дней]
        # [Назад в меню]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_GRAPH, caption_message_text)
        # User > [try_level] = min,average,max
        await resp.click(text=try_level)

        caption_message_text = f'submenu: for_shop\n' \
                               f'shop: {shop_name}\n' \
                               f'vendor: \n' \
                               f'arch: {arch_name}\n' \
                               f'series: {next_series}\n' \
                               f'days: {try_days.split(" ")[0]}\n' \
                               f'level: {level_dict.get(try_level)}\n' + select_graph_text

        # Bot < caption_message + Выберите вид графика:
        # [Мин][Среднее][Макс]
        # [30 дней][60 дней][90 дней]
        # [Назад в меню]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_GRAPH, caption_message_text)
        # User > [Назад в меню]
        await resp.click(text=keyboard_GRAPH[2][0].text)

        # Bot < Чтобы получить информацию, воспользуйся кнопками:
        # [Статистика цен][Популярность видеокарт]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)


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
async def test_for_shop_stats_missing(client: TelegramClient, shop_name, arch_name,
                                      series_name, missing_series):
    async with client.conversation('@GpuPricesBot', timeout=10) as conv:
        # User > /start
        await conv.send_message("/start")

        # Bot < Привет, {user}!
        await conv.get_response()

        # Bot < Я информационный бот, который поможет тебе узнать цены
        # на видеокарты в различных магазинах!
        await conv.get_response()

        # Bot < Чтобы получить информацию, воспользуйся кнопками:
        # [Статистика цен][Популярность видеокарт]
        resp = await conv.get_response()
        # User > [Статистика цен]
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите вид статистики:
        # [По Магазину][По Производителю][По Видеокарте]
        resp = await get_last_message(client, conv, timeout=5)
        # User > [По Магазину]
        await resp.click(text=keyboard_STATS[0][0].text)

        # Bot < Выберите магазин:
        # [DNS][MVIDEO][CITILINK]
        resp = await get_last_message(client, conv, timeout=5)
        # User > [shop_name]
        await resp.click(text=shop_name)

        # Bot < Выберите архитектуру видеокарты:
        # [NVIDIA][AMD]
        # [Другие]
        resp = await get_last_message(client, conv, timeout=5)
        # User > [arch_name]
        await resp.click(text=arch_name)

        # Bot < Выберите серию видеокарт:
        # NVIDIA
        # [Geforce 10XX][Geforce 16XX]
        # [Geforce 20XX][Geforce 30XX]
        # [Geforce 40XX][Другие]
        # AMD
        # [Radeon RX 5XX][Radeon RX 5XXX]
        # [Radeon RX 6XXX][Другие]
        # Другие
        # [INTEL][MATROX]
        resp = await get_last_message(client, conv, timeout=5)
        # User > [series_name]
        await resp.click(text=series_name)

        # Bot < Выберите серию видеокарт:
        # NVIDIA - Geforce 10XX
        # [GeForce GTX 1080 TI][GeForce GTX 1050 TI][GeForce GT 1030]
        # AMD - Radeon RX 5XX
        # [Radeon RX 550][Radeon RX 560][Radeon RX 580]
        # INTEL
        # [Arc A310][Arc A380]
        resp = await get_last_message(client, conv, timeout=5)
        # User > [missing_series]
        await resp.click(text=missing_series)

        # Bot < Нет данных по выбранным параметрам
        # [Назад в Меню]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_ONLY_BACK, no_data_text)
        # User > [Назад в меню]
        await resp.click(text=keyboard_GRAPH[2][0].text)

        # Bot < Чтобы получить информацию, воспользуйся кнопками:
        # [Статистика цен][Популярность видеокарт]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)


@pytest.mark.system
@mark.asyncio
async def test_for_shop_stats_out_dialog(client: TelegramClient):
    async with client.conversation('@GpuPricesBot', timeout=10) as conv:
        # User > /start
        await conv.send_message("/start")

        # Bot < Привет, {user}!
        await conv.get_response()

        # Bot < Я информационный бот, который поможет тебе узнать цены
        # на видеокарты в различных магазинах!
        await conv.get_response()

        # Bot < Чтобы получить информацию, воспользуйся кнопками:
        # [Статистика цен][Популярность видеокарт]
        resp = await conv.get_response()
        # User > [Статистика цен]
        await resp.click(text=keyboard_MENU[0][0].text)

        # Bot < Выберите вид статистики:
        # [По Магазину][По Производителю][По Видеокарте]
        resp = await get_last_message(client, conv, timeout=5)
        # User > [По Магазину]
        await resp.click(text=keyboard_STATS[0][0].text)

        # Bot < Выберите магазин:
        # [DNS][MVIDEO][CITILINK]
        resp = await get_last_message(client, conv, timeout=5)
        # User > random message
        await conv.send_message('random message')

        # Bot < Ошибка! Необходимо выбрать кнопку.
        resp_error: Message = await conv.get_response()
        assert error_enter_text in resp_error.raw_text
        # User > [DNS]
        await resp.click(text=keyboard_SHOPS[0][0].text)

        # Bot < Выберите архитектуру видеокарты:
        # [NVIDIA][AMD]
        # [Другие]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_ARCHITECTURES, select_arch_text)
        # User > random message
        await conv.send_message('random message')

        # Bot < Ошибка! Необходимо выбрать кнопку.
        resp_error: Message = await conv.get_response()
        assert error_enter_text in resp_error.raw_text
        # User > [NVIDIA]
        await resp.click(text=keyboard_ARCHITECTURES[0][0].text)

        # Bot < Выберите серию видеокарт:
        # NVIDIA
        # [Geforce 10XX][Geforce 16XX]
        # [Geforce 20XX][Geforce 30XX]
        # [Geforce 40XX][Другие]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_NVIDIA_SERIES, select_series_text)
        # User > random message
        await conv.send_message('random message')

        # Bot < Ошибка! Необходимо выбрать кнопку.
        resp_error: Message = await conv.get_response()
        assert error_enter_text in resp_error.raw_text
        # User > [Geforce 10XX]
        await resp.click(text=keyboard_NVIDIA_SERIES[0][0].text)

        # Bot < Выберите серию видеокарт:
        # [GeForce GTX 1080 TI][GeForce GTX 1050 TI][GeForce GT 1030]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_NVIDIA_10XX_SERIES, select_series_text)
        # User > random message
        await conv.send_message('random message')

        # Bot < Ошибка! Необходимо выбрать кнопку.
        resp_error: Message = await conv.get_response()
        assert error_enter_text in resp_error.raw_text
        # User > [GeForce GTX 1080 TI]
        await resp.click(text=keyboard_NVIDIA_10XX_SERIES[0][0].text)

        # Bot < Нет данных по выбранным параметрам
        # [Назад в Меню]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_ONLY_BACK, no_data_text)
        # User > random message
        await conv.send_message('random message')

        # Bot < Ошибка! Необходимо выбрать кнопку.
        resp_error: Message = await conv.get_response()
        assert error_enter_text in resp_error.raw_text
        # User > [Назад в меню]
        await resp.click(text=keyboard_GRAPH[2][0].text)

        # Bot < Чтобы получить информацию, воспользуйся кнопками:
        # [Статистика цен][Популярность видеокарт]
        resp = await get_last_message(client, conv, timeout=5)
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)


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


async def get_last_message(client: TelegramClient, conv: Conversation, timeout=0.5):
    time.sleep(timeout)
    messages_list = await client.get_messages(conv.chat)
    return messages_list[0]
