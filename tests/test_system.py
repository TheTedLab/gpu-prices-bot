import time
import pytest
from pytest import mark
from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.custom.conversation import Conversation
from src.bot.constants import *

# Запуск в командной строке из папки tests
# cd tests
# Далее запуск тестов с маркером system без покрытия (no-cov)
# pytest -m system --no-cov
# Можно добавить -s для просмотра вывода (если нужно смотреть print'ы)
# pytest -m system --no-cov -s

@pytest.mark.system
@mark.asyncio
async def test_start(client: TelegramClient):
    # Создание разговора с ботом (необходимо в каждом тесте)
    async with client.conversation('@GpuPricesBot', timeout=5) as conv:
        # Отправка команды или любого сообщения
        # User > /start
        await conv.send_message("/start")

        # Получение ответа
        # Bot < Привет, {user}!
        resp: Message = await conv.get_response()
        assert "Привет" in resp.raw_text

        # Bot < Я информационный бот, который поможет тебе узнать оценки рецензии на различные видеоигры!
        # Чтобы получить информацию, просто напиши название игры!
        resp = await conv.get_response()
        assert greetings_text in resp.raw_text

        # Проверка клавиатуры
        resp = await conv.get_response()
        await check_keyboard(resp, keyboard_MENU, using_buttons_text)

        # Как нажать кнопку (нужно сделать 'resp = await conv.get_response()' до этого)
        await resp.click(text=keyboard_MENU[0][0].text)
        # Тем не менее не нужно делать это конкретно здесь так как resp получен до клавиатуры
        # Если сделать resp = await лишний раз то получится пустое сообщение

        # Последний вызов лучше получать через функцию
        resp = await get_last_message(client, conv)
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
@pytest.mark.parametrize('arch_0, arch_1', params_parchitecture_submenu)
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
            await resp.click(text=card_architecture_1)


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
