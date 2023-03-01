import pytest
import pendulum
import telegram
from loguru import logger
from operator import eq

from src.bot.commands import *
from src.bot.constants import *
from telegram import InlineKeyboardMarkup


@pytest.mark.bot
def test_set_datetime():
    logger.configure(patcher=set_datetime)
    record = {"extra": {}}
    logger.__dict__['_core'].patcher(record)
    expected_record = {'extra': {'datetime': pendulum.now('Europe/Moscow').strftime('%Y-%m-%dT%H:%M:%S')}}
    assert record == expected_record

@pytest.mark.bot
def test_start(mocked_update_context, mocker):
    mocked_update, mocked_context = mocked_update_context
    start(mocked_update, mocked_context)
    print()

    test_username = mocked_update.message.from_user.full_name.encode(encoding='utf-8').decode()

    expected_context_calls = [
        mocker.call(CURRENT_SUBMENU, ''),
        mocker.call(CURRENT_SHOP, ''),
        mocker.call(CURRENT_ARCH, ''),
        mocker.call(CURRENT_VENDOR, ''),
        mocker.call(CURRENT_GPU, ''),
        mocker.call(CURRENT_GRAPH_LEVEL, 0),
        mocker.call(CURRENT_GRAPH_DAYS, 30),
        mocker.call(CURRENT_GRAPH_STATE, 8),
        mocker.call(CURRENT_GRAPH_START, 0),
        mocker.call(CURRENT_TEMP_DATA, ''),
        mocker.call(CURRENT_USER_NAME, ''),
        mocker.call(CURRENT_USER_NAME, test_username)
    ]

    mocked_context.user_data.__setitem__.assert_has_calls(expected_context_calls)

    expected_update_calls_reply_text = [
        mocker.call(text=hello_text + f'{test_username}!'),
        mocker.call(text=greetings_text)
    ]

    mocked_update.message.reply_text.assert_has_calls(expected_update_calls_reply_text)

    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)

    assert reply_markup_keyboard == mocked_update.message.reply_photo.call_args.kwargs['reply_markup']
    assert using_buttons_text == mocked_update.message.reply_photo.call_args.kwargs['caption']


@pytest.mark.bot
def test_start_over(mocked_update_context, mocker, shops_logo_path):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'

    start_over(mocked_update, mocked_context)
    print()
    # print(mocked_context.user_data.mock_calls)
    # print(mocked_context.user_data.__setitem__.mock_calls)
    # print(mocked_context.user_data.__getitem__.mock_calls)

    expected_context_set_calls = [
        mocker.call(CURRENT_SUBMENU, ''),
        mocker.call(CURRENT_SHOP, ''),
        mocker.call(CURRENT_ARCH, ''),
        mocker.call(CURRENT_VENDOR, ''),
        mocker.call(CURRENT_GPU, ''),
        mocker.call(CURRENT_GRAPH_LEVEL, 0),
        mocker.call(CURRENT_GRAPH_DAYS, 30),
        mocker.call(CURRENT_GRAPH_STATE, 8),
        mocker.call(CURRENT_GRAPH_START, 0),
        mocker.call(CURRENT_TEMP_DATA, ''),
        mocker.call(CURRENT_USER_NAME, ''),
        mocker.call(CURRENT_USER_NAME, 'Tester')
    ]

    mocked_context.user_data.__setitem__.assert_has_calls(expected_context_set_calls)

    expected_context_get_calls = [
        mocker.call(30)
    ]

    mocked_context.user_data.__getitem__.assert_has_calls(expected_context_get_calls)

    with open(shops_logo_dir, 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)

    expected_update_calls = [
        mocker.call.answer(),
        mocker.call.edit_message_media(media=image),
        mocker.call.edit_message_caption(
            caption=using_buttons_text,
            reply_markup=reply_markup_keyboard
        )
    ]

    # print(expected_update_calls)
    # print(mocked_update.callback_query.mock_calls)

    mocked_update.callback_query.assert_has_calls(expected_update_calls)

@pytest.mark.bot
def test_reset_context(mocked_update_context, mocker):
    mocked_update, mocked_context = mocked_update_context

    reset_context(mocked_context)

    # print(mocked_context.user_data.__setitem__.mock_calls)
