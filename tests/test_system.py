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
