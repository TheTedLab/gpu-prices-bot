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

    return_value = start(mocked_update, mocked_context)

    assert return_value == MENU

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

    return_value = start_over(mocked_update, mocked_context)

    assert return_value == MENU

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
        mocker.call(CURRENT_USER_NAME, '')
    ]

    mocked_context.user_data.__setitem__.assert_has_calls(expected_context_calls)


params_to_try = (
    (keyboard_MENU, using_buttons_text, CURRENT_TEMP_DATA),
    (keyboard_SHOPS, select_shop_text, CURRENT_SUBMENU),
    (keyboard_VENDORS, select_vendor_text, CURRENT_SUBMENU)
)

params_ids = [
    f'keyboard_{params_to_try.index(par)}, ' \
    f'caption_text_{params_to_try.index(par)}, ' \
    f'{par[2]}' for par in params_to_try
]
@pytest.mark.bot
@pytest.mark.parametrize('keyboard, caption_text, current_const', params_to_try, ids=params_ids)
def test_update_query_message_with_keyboard(mocked_update_context, mocker,
        keyboard, caption_text, current_const):
    mocked_update, mocked_context = mocked_update_context

    update_query_message_with_keyboard(
        update=mocked_update,
        context=mocked_context,
        keyboard=keyboard,
        image_path=shops_logo_dir,
        caption_text=caption_text,
        current_const=current_const
    )

    expected_context_calls = [
        mocker.call(current_const, mocked_update.callback_query.data)
    ]

    mocked_context.user_data.__setitem__.assert_has_calls(expected_context_calls)

    with open(shops_logo_dir, 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    reply_markup_keyboard = InlineKeyboardMarkup(keyboard)

    expected_update_calls = [
        mocker.call.answer(),
        mocker.call.edit_message_media(media=image),
        mocker.call.edit_message_caption(
            caption=caption_text,
            reply_markup=reply_markup_keyboard
        )
    ]

    mocked_update.callback_query.assert_has_calls(expected_update_calls)

params_for_shop_try = (
    (FOR_SHOP, SHOPS_SUBMENU, CURRENT_SUBMENU, select_shop_text, keyboard_SHOPS),
    (FOR_VENDOR, VENDORS_SUBMENU, CURRENT_SUBMENU, select_vendor_text, keyboard_VENDORS),
    (FOR_GPU, MENU, CURRENT_TEMP_DATA, using_buttons_text, keyboard_MENU)
)

params_for_shop_ids = [
    f'submenu:{par[0]}, r_val:{par[1]}, const:{par[2]},' \
    f' caption:{params_for_shop_try.index(par)},' \
    f' keyboard:{params_for_shop_try.index(par)}' for par in params_for_shop_try
]

@pytest.mark.bot
@pytest.mark.parametrize('submenu, r_val, current_const, caption, keyboard',
                         params_for_shop_try, ids=params_for_shop_ids)
def test_for_shop_vendor_stats(mocked_update_context, mocker,
        submenu, r_val, current_const, caption, keyboard):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'
    mocked_update.callback_query.data = str(submenu)

    return_value = for_shop_vendor_stats(mocked_update, mocked_context)
    assert return_value == r_val

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__getitem__(CURRENT_USER_NAME),
        mocker.call.__setitem__(current_const, str(submenu))
    ]

    mocked_context.user_data.assert_has_calls(expected_context_calls)

    with open(shops_logo_dir, 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    reply_markup_keyboard = InlineKeyboardMarkup(keyboard)

    expected_update_calls = [
        mocker.call.answer(),
        mocker.call.edit_message_media(media=image),
        mocker.call.edit_message_caption(
            caption=caption,
            reply_markup=reply_markup_keyboard
        )
    ]

    mocked_update.callback_query.assert_has_calls(expected_update_calls)
