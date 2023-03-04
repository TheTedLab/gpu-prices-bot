import json

import pytest
import filecmp
import pathlib
import requests_mock

from src.bot.commands import *
from src.bot.constants import *
from telegram import InlineKeyboardMarkup
import colorsys


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
def test_start_over(mocked_update_context, mocker):
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

params_for_popularity = (
    (POPULARITY_FOR_SHOP, POPULARITY_SHOPS_SUBMENU, select_shop_text, keyboard_SHOPS),
    (POPULARITY_FOR_VENDOR, POPULARITY_VENDORS_SUBMENU, select_vendor_text, keyboard_VENDORS),
    (FOR_GPU, MENU, using_buttons_text, keyboard_MENU)
)

params_for_popularity_ids = [
    f'submenu:{par[0]}, r_val:{par[1]}' for par in params_for_popularity
]

@pytest.mark.bot
@pytest.mark.parametrize('submenu, r_val, caption, keyboard',
                         params_for_popularity, ids=params_for_popularity_ids)
def test_for_shop_vendor_popularity(mocked_update_context, mocker,
                                    submenu, r_val, caption, keyboard):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'
    mocked_update.callback_query.data = str(submenu)

    return_value = for_shop_vendor_popularity(mocked_update, mocked_context)
    assert return_value == r_val

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__getitem__(CURRENT_USER_NAME),
        mocker.call.__setitem__(CURRENT_TEMP_DATA, str(submenu))
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


@pytest.mark.bot
def test_for_gpu(mocked_update_context, mocker):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'

    return_value = for_gpu(mocked_update, mocked_context)
    assert return_value == GPU_SUBMENU

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__getitem__(CURRENT_USER_NAME),
        mocker.call.__setitem__(CURRENT_GRAPH_GPU_LEVEL, 0),
        mocker.call.__setitem__(CURRENT_GRAPH_GPU_DAYS, 30),
        mocker.call.__setitem__(CURRENT_GRAPH_GPU_STATE, 16),
        mocker.call.__setitem__(CURRENT_GRAPH_GPU_START, 0),
        mocker.call.__setitem__(CURRENT_TEMP_DATA, mocked_update.callback_query.data)
    ]

    mocked_context.user_data.assert_has_calls(expected_context_calls)

    with open(shops_logo_dir, 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_EMPTY)

    expected_update_calls = [
        mocker.call.answer(),
        mocker.call.edit_message_media(media=image),
        mocker.call.edit_message_caption(
            caption=select_gpu_text,
            reply_markup=reply_markup_keyboard
        )
    ]

    mocked_update.callback_query.assert_has_calls(expected_update_calls)


params_update_data = [
    str(i) for i in [
        AMD_RX5XX_SERIES, AMD_RX5XXX_SERIES, AMD_RX6XXX_SERIES, AMD_OTHER_SERIES,
        AMD_RX_66XX_SERIES, AMD_RX_67XX_SERIES, AMD_RX_68XX_SERIES, AMD_RX_69XX_SERIES,
        NVIDIA_QUADRO_RTX_AXXXX_SERIES, ''
    ]
]

@pytest.mark.bot
@pytest.mark.parametrize('update_data', params_update_data)
def test_amd_series_func(mocked_update_context, mocker, update_data):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'
    mocked_update.callback_query.data = update_data

    return_value = amd_series_func(mocked_update, mocked_context)
    r_val = series_buttons_dict.get(int(update_data))['returning'] if update_data != '' else MENU
    assert return_value == r_val

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__getitem__(CURRENT_USER_NAME),
        mocker.call.__setitem__(CURRENT_TEMP_DATA, update_data)
    ]

    mocked_context.user_data.assert_has_calls(expected_context_calls)

    with open(shops_logo_dir, 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    keyboard = series_buttons_dict.get(int(update_data))['keyboard'] if update_data != '' else keyboard_ONLY_BACK
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard)

    expected_update_calls = [
        mocker.call.answer(),
        mocker.call.edit_message_media(media=image),
        mocker.call.edit_message_caption(
            caption=select_series_text,
            reply_markup=reply_markup_keyboard
        )
    ]

    mocked_update.callback_query.assert_has_calls(expected_update_calls)


gpu_lists_to_try = (
        (['GEFORCE RTX 4080 EAGLE OC 16GB'], 0),
        (['GEFORCE RTX 3070 8GB DUAL FAN', 'GEFORCE RTX 3070 VENTUS 3X 8G 256B'], 0),
        (['GEFORCE RTX 3070 8GB DUAL FAN', 'GEFORCE RTX 3070 VENTUS 3X 8G 256B'], 1),
        (
            [
                'RADEON RX 6600 XT 8GB NITRO+',
                'ASUS DUAL RADEON RX 6600 XT OC EDITION',
                'GIGABYTE AMD RADEON RX 6600 XT GAMING OC'
            ],
            0
        ),
        (
            [
                'ASUS GEFORCE GTX 1660 SUPER PHOENIX',
                'INNO3D GEFORCE GTX 1660 SUPER TWIN X2',
                'GEFORCE GTX 1660 SUPER GP 6G'
            ],
            1
        ),
        (
            [
                'GEFORCE RTX 3060 TI DUAL 8GB',
                'GEFORCE RTX 3060 TI PA-RTX3060 DUAL 8G',
                'GEFORCE RTX 3060 TI GAMING X 8G'
            ],
            2
        )
)

gpu_lists_ids = [
    f'gpu_list_{gpu_lists_to_try.index(gpu_list)},' \
    f' pressed_button_index: {gpu_list[1]}' for gpu_list in gpu_lists_to_try
]

@pytest.mark.bot
@pytest.mark.parametrize('gpu_list, pressed_button_index', gpu_lists_to_try, ids=gpu_lists_ids)
def test_gpu_info(mocked_update_context, mocker, gpu_list, pressed_button_index):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'
    print()
    inline_keyboard_gpu_search_buttons(gpu_search=gpu_list)

    mocked_update.callback_query.data = \
        keyboard_ON_SEARCH[pressed_button_index][0].callback_data

    return_value = gpu_info(mocked_update, mocked_context)

    assert return_value == GRAPH_SUBMENU_ON_GPU

    print(gpu_list)
    print(gpu_list[pressed_button_index])
    print(keyboard_ON_SEARCH[pressed_button_index][0])

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__setitem__(CURRENT_DATA, gpu_list[pressed_button_index]),
        mocker.call.__getitem__(CURRENT_USER_NAME),
        mocker.call.__setitem__(CURRENT_GPU, gpu_list[pressed_button_index])
    ]

    mocked_context.user_data.assert_has_calls(expected_context_calls)

    with open(shops_logo_dir, 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_GRAPH_PERIODS)

    expected_update_calls = [
        mocker.call.edit_message_media(media=image),
        mocker.call.edit_message_caption(
            caption=select_graph_text,
            reply_markup=reply_markup_keyboard
        )
    ]

    mocked_update.callback_query.assert_has_calls(expected_update_calls)

params_for_inline = (
    ['GEFORCE RTX 4080 EAGLE OC 16GB'],
    ['GEFORCE RTX 3070 8GB DUAL FAN', 'GEFORCE RTX 3070 VENTUS 3X 8G 256B'],
    ['GEFORCE RTX 4080 EAGLE OC 16GB', 'GEFORCE RTX 4080 EAGLE OC 16GB'],
    [
        'RADEON RX 6600 XT 8GB NITRO+',
        'ASUS DUAL RADEON RX 6600 XT OC EDITION',
        'GIGABYTE AMD RADEON RX 6600 XT GAMING OC'
    ]
)

@pytest.mark.bot
@pytest.mark.parametrize('gpu_list_search', params_for_inline)
def test_inline_keyboard(gpu_list_search):
    inline_keyboard_gpu_search_buttons(gpu_list_search)

    for button_list_i in range(len(keyboard_ON_SEARCH)):
        assert gpu_list_search[button_list_i] == keyboard_ON_SEARCH[button_list_i][0].text
        assert keyboard_ON_SEARCH[button_list_i][0].callback_data == f'[\'gpu\', \'{button_list_i}\']'


params_for_gpu_search_func = (
    ('GEFORCE RTX 4080 EAGLE OC 16GB', True, 200),
    ('GEFORCE RTX 4040', False, 404),
    ('', False, 404),
    ('GEFORCE RTX 3070 8GB DUAL FAN', True, 200),
    ('hello world', False, 404)
)

@pytest.mark.bot
@pytest.mark.parametrize('gpu_test_name, json_data, status_code', params_for_gpu_search_func)
def test_gpu_search_func(mocked_update_context, mocker,
                         requests_mock, gpu_test_name, json_data, status_code):
    mocked_update, mocked_context = mocked_update_context

    mocked_update.message.text = gpu_test_name
    mocked_update.message.from_user.full_name = 'Tester'

    url = f'http://173.18.0.3:8080/is-card-present?cardName={gpu_test_name}'

    requests_mock.get(url, json=json_data, status_code=status_code)

    return_value = gpu_search_func(mocked_update, mocked_context)
    assert return_value == ON_SEARCH if status_code == 200 else ON_GPU_QUESTION

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_DATA, gpu_test_name),
        mocker.call.__getitem__(CURRENT_DATA)
    ]

    mocked_context.user_data.assert_has_calls(expected_context_calls)

    caption_text = search_results_for_text + gpu_test_name + ": " if status_code == 200 else no_search_results_text
    keyboard = keyboard_ON_SEARCH if status_code == 200 else keyboard_ONLY_BACK
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard)

    assert reply_markup_keyboard == mocked_update.message.reply_photo.call_args.kwargs['reply_markup']
    assert caption_text == mocked_update.message.reply_photo.call_args.kwargs['caption']
    
params_stats_popularity_func_try = (
    (STATS, STATS_SUBMENU, select_stats_text, keyboard_STATS),
    (POPULARITY, POPULARITY_SUBMENU, select_popularity_text, keyboard_POPULARITY),
    (FOR_GPU, MENU, using_buttons_text, keyboard_MENU)
)

params_stats_popularity_func_ids = [
    f'submenu:{par[0]}, r_val:{par[1]},' \
    f' caption:{params_stats_popularity_func_try.index(par)},' \
    f' keyboard:{params_stats_popularity_func_try.index(par)}' for par in params_stats_popularity_func_try
]


@pytest.mark.bot
@pytest.mark.parametrize('submenu, r_val, caption, keyboard',
                         params_stats_popularity_func_try, ids=params_stats_popularity_func_ids)
def test_stats_popularity_func(mocked_update_context, mocker,
                               submenu, r_val, caption, keyboard):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'
    mocked_update.callback_query.data = str(submenu)

    return_value = stats_popularity_func(mocked_update, mocked_context)
    assert return_value == r_val

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__getitem__(CURRENT_USER_NAME)
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


@pytest.mark.bot
def test_get_random_color():
    r_val = get_random_color()

    assert isinstance(r_val, tuple)

    hsv = colorsys.rgb_to_hsv(r_val[0], r_val[1], r_val[2])
    for col in hsv:
        assert col <= 1
    assert hsv[0] >= 0.0
    assert hsv[1] >= 0.2
    assert hsv[2] >= 0.9

@pytest.mark.bot
def test_define_popularity_places_shops(graph_data, vendor):

    expected_message_caption = "Популярность по производителю Vendor A:\n"
    expected_message_caption += shops_emojis_dict.get("MVIDEO") + " MVIDEO\n"
    expected_message_caption += "1. Product A\n"
    expected_message_caption += "2. Product B\n"
    expected_message_caption += "3. No Data\n\n"
    expected_message_caption += shops_emojis_dict.get("CITILINK") + " CITILINK\n"
    expected_message_caption += "1. No Data\n"
    expected_message_caption += "2. Product C\n"
    expected_message_caption += "3. Product D\n\n"

    expected_popularity_places_shops = {
        "CITILINK": ["Product D", "Product C", "No Data"],
        "MVIDEO": ["No Data", "Product B", "Product A"]
    }

    result_message_caption, result_popularity_places_shops = define_popularity_places_shops(graph_data, vendor)

    assert result_message_caption == expected_message_caption
    assert result_popularity_places_shops == expected_popularity_places_shops


params_nvidia_amd_other_func_try = (
    (NVIDIA, NVIDIA_SERIES_SUBMENU, CURRENT_ARCH, select_series_text, keyboard_NVIDIA_SERIES),
    (AMD, AMD_SERIES_SUBMENU, CURRENT_ARCH, select_series_text, keyboard_AMD_SERIES),
    (OTHER_ARCH, OTHER_ARCH_SUBMENU, CURRENT_TEMP_DATA, select_arch_text, keyboard_OTHER_ARCH),
    (INTEL, INTEL_SERIES_SUBMENU, CURRENT_ARCH, select_series_text, keyboard_INTEL_SERIES),
    (MATROX, MATROX_SERIES_SUBMENU, CURRENT_ARCH, select_series_text, keyboard_MATROX_SERIES),
    (AMD_RX_67XX_SERIES, MENU, CURRENT_TEMP_DATA, using_buttons_text, keyboard_MENU)
)

params_nvidia_amd_other_func_ids = [
    f'submenu:{par[0]}, r_val:{par[1]}, const:{par[2]},' \
    f' caption:{params_nvidia_amd_other_func_try.index(par)},' \
    f' keyboard:{params_nvidia_amd_other_func_try.index(par)}' for par in params_nvidia_amd_other_func_try
]
@pytest.mark.bot
@pytest.mark.parametrize('submenu, r_val, current_const, caption, keyboard',
                         params_nvidia_amd_other_func_try, ids=params_nvidia_amd_other_func_ids)
def test_nvidia_amd_other_func(mocked_update_context, mocker,
                               submenu, r_val, current_const, caption, keyboard):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'
    mocked_update.callback_query.data = str(submenu)

    return_value = nvidia_amd_other_func(mocked_update, mocked_context)
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


params_arch_func_try = (
    (FOR_SHOP, ARCHITECTURE_SUBMENU, CURRENT_SHOP, select_arch_text, keyboard_ARCHITECTURES, DNS_SHOP),
    (FOR_SHOP, ARCHITECTURE_SUBMENU, CURRENT_SHOP, select_arch_text, keyboard_ARCHITECTURES, CITILINK_SHOP),
    (FOR_SHOP, ARCHITECTURE_SUBMENU, CURRENT_SHOP, select_arch_text, keyboard_ARCHITECTURES, MVIDEO_SHOP),
    (FOR_VENDOR, ARCHITECTURE_SUBMENU, CURRENT_VENDOR, select_arch_text, keyboard_ARCHITECTURES, VENDOR_PALIT),
    (FOR_VENDOR, ARCHITECTURE_SUBMENU, CURRENT_VENDOR, select_arch_text, keyboard_ARCHITECTURES, VENDOR_ASUS),
    (FOR_VENDOR, ARCHITECTURE_SUBMENU, CURRENT_VENDOR, select_arch_text, keyboard_ARCHITECTURES, VENDOR_MSI),
    (FOR_GPU, MENU, CURRENT_TEMP_DATA, using_buttons_text, keyboard_MENU, 0)
)

params_arch_func_ids = [
    f'submenu:{par[0]}, r_val:{par[1]}, const:{par[2]},' \
    f' caption:{params_arch_func_try.index(par)},' \
    f' keyboard:{params_arch_func_try.index(par)}' \
    f' shop:{par[5]}' for par in params_arch_func_try
]
@pytest.mark.bot
@pytest.mark.parametrize('submenu, r_val, current_const, caption, keyboard, query_data',
                         params_arch_func_try, ids=params_arch_func_ids)
def test_arch_func(mocked_update_context, mocker,
                   submenu, r_val, current_const, caption, keyboard, query_data):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'
    mocked_context.user_data[CURRENT_SUBMENU] = str(submenu)
    mocked_update.callback_query.data = str(query_data)

    return_value = arch_func(mocked_update, mocked_context)
    assert return_value == r_val

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__setitem__(CURRENT_SUBMENU, str(submenu)),
        mocker.call.__getitem__(CURRENT_USER_NAME),
        mocker.call.__getitem__(CURRENT_SUBMENU),
        mocker.call.__setitem__(current_const, str(query_data))
    ]

    if submenu in [FOR_SHOP, FOR_VENDOR]:
        expected_context_calls.append(mocker.call.__getitem__(current_const))

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

@pytest.mark.bot
def test_help_func(mocked_update_context):
    mocked_update, mocked_context = mocked_update_context
    help_func(mocked_update, mocked_context)

    assert mocked_update.message.reply_text.called_once_with(text=help_text)

@pytest.mark.bot
def test_end_on_gpu(mocked_update_context):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'

    assert end_on_gpu(mocked_update, mocked_context) == BACK_TO_MENU
    assert mocked_update.called_once_with(mocked_update, mocked_context)

@pytest.mark.bot
def test_start_fallback(mocked_update_context):
    mocked_update, mocked_context = mocked_update_context
    assert start_fallback(mocked_update, mocked_context) == BACK_TO_MENU


@pytest.mark.bot
def test_new_start(mocked_update_context, mocker):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'

    return_value = new_start(mocked_update, mocked_context)
    assert return_value == MENU

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__getitem__(CURRENT_USER_NAME),
        mocker.call.__setitem__(CURRENT_TEMP_DATA, mocked_update.callback_query.data)
    ]

    mocked_context.user_data.assert_has_calls(expected_context_calls)

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

    mocked_update.callback_query.assert_has_calls(expected_update_calls)


params_update_data_nvidia = [
    str(i) for i in [
        NVIDIA_10XX_SERIES, NVIDIA_16XX_SERIES, NVIDIA_20XX_SERIES, NVIDIA_30XX_SERIES,
        NVIDIA_40XX_SERIES, NVIDIA_OTHER_SERIES, NVIDIA_QUADRO_SERIES, NVIDIA_TESLA_SERIES,
        ''
    ]
]


@pytest.mark.bot
@pytest.mark.parametrize('update_data', params_update_data_nvidia)
def test_nvidia_series_func(mocked_update_context, mocker, update_data):
    mocked_update, mocked_context = mocked_update_context
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'
    mocked_update.callback_query.data = update_data

    return_value = nvidia_series_func(mocked_update, mocked_context)
    r_val = series_buttons_dict.get(int(update_data))['returning'] if update_data != '' else MENU
    assert return_value == r_val

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__getitem__(CURRENT_USER_NAME),
        mocker.call.__setitem__(CURRENT_TEMP_DATA, update_data)
    ]

    mocked_context.user_data.assert_has_calls(expected_context_calls)

    with open(shops_logo_dir, 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    keyboard = series_buttons_dict.get(int(update_data))['keyboard'] if update_data != '' else keyboard_ONLY_BACK
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard)

    expected_update_calls = [
        mocker.call.answer(),
        mocker.call.edit_message_media(media=image),
        mocker.call.edit_message_caption(
            caption=select_series_text,
            reply_markup=reply_markup_keyboard
        )
    ]

    mocked_update.callback_query.assert_has_calls(expected_update_calls)

@pytest.mark.bot
def test_get_days_list():
    base = datetime.date(2022, 11, 20)
    now = datetime.datetime.today().date()
    days = [str(base + datetime.timedelta(days=x)) for x in range((now - base).days + 1)]
    assert get_days_list() == days


params_define_prices = (
    (get_days_list(), 'min', {}, ["PALIT", "ASUS"]),
    (get_days_list(), 'max', {}, ["PALIT", "ASUS"]),
    (get_days_list(), 'average', {}, ["PALIT", "ASUS"]),
    (get_days_list(), 'hello', {}, ["PALIT", "ASUS"]),
)


@pytest.mark.bot
@pytest.mark.parametrize('days, graph_level, prices, shops_names', params_define_prices)
def test_define_prices_by_graph_level(days, graph_level, graph_offers_vendors_data, prices, shops_names):
    r_mode = define_prices_by_graph_level(days, graph_level, graph_offers_vendors_data, prices, shops_names)
    assert r_mode == graph_level


@pytest.mark.bot
def test_error_attention(mocked_update_context, mocker):
    mocked_update, mocked_context = mocked_update_context
    mocked_update.message.from_user.full_name = 'Tester'

    error_attention(mocked_update, mocked_context)

    expected_update_calls = [
        mocker.call(text=error_enter_text)
    ]

    mocked_update.message.reply_text.assert_has_calls(expected_update_calls)


params_popularity_shops_graph = [
    (DNS_SHOP, 'DNS'),
    (MVIDEO_SHOP, 'MVIDEO'),
    (CITILINK_SHOP, 'CITILINK')
]

@pytest.mark.bot
@pytest.mark.parametrize('shop_const, shop_name', params_popularity_shops_graph)
def test_popularity_shops_graph(mocked_update_context, mocker, requests_mock,
                                shop_const, shop_name):
    mocked_update, mocked_context = mocked_update_context
    mocked_update.callback_query.data = str(shop_const)
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'

    url = f'http://173.18.0.3:8080/popularity/for-shop?shopName={shop_name}'

    with open(f'resources/popularity-shops-graph-data-{shop_name}.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    requests_mock.get(url, json=json_data)

    return_value = popularity_shops_graph(mocked_update, mocked_context)
    assert return_value == POPULARITY_SHOPS_GRAPH_SUBMENU

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__getitem__(CURRENT_USER_NAME),
        mocker.call.__setitem__(CURRENT_TEMP_DATA, str(shop_const))
    ]

    mocked_context.user_data.assert_has_calls(expected_context_calls)

    with open('graphic.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_POPULARITY_GRAPH)

    expected_update_calls = [
        mocker.call.answer(),
        mocker.call.edit_message_media(media=image),
        mocker.call.edit_message_caption(
            caption=popularity_shop_text + shop_name,
            reply_markup=reply_markup_keyboard
        )
    ]

    mocked_update.callback_query.assert_has_calls(expected_update_calls)


params_popularity_vendors_graph = [
    (VENDOR_MSI, 'MSI'),
    (VENDOR_ASUS, 'ASUS'),
    (VENDOR_PALIT, 'PALIT')
]


@pytest.mark.bot
@pytest.mark.parametrize('vendor_const, vendor_name', params_popularity_vendors_graph)
def test_popularity_vendors_graph(mocked_update_context, mocker, requests_mock,
                                vendor_const, vendor_name):
    mocked_update, mocked_context = mocked_update_context
    mocked_update.callback_query.data = str(vendor_const)
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'

    url = f'http://173.18.0.3:8080/popularity/for-vendor?vendorName={vendor_name}'

    with open(f'resources/popularity-vendors-graph-data-{vendor_name}.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    requests_mock.get(url, json=json_data)

    return_value = popularity_vendors_graph(mocked_update, mocked_context)
    assert return_value == POPULARITY_VENDORS_GRAPH_SUBMENU

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__getitem__(CURRENT_USER_NAME),
        mocker.call.__setitem__(CURRENT_TEMP_DATA, str(vendor_const))
    ]

    mocked_context.user_data.assert_has_calls(expected_context_calls)

    with open('graphic.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    expected_message_caption = popularity_vendor_text + vendor_name + ':\n'
    for shop in json_data:
        expected_message_caption += shops_emojis_dict.get(shop) + f" {shop}\n"
        for place in ['1', '2', '3']:
            if json_data[shop].get(place) is not None:
                card_name = json_data[shop][place]['cardName']
                expected_message_caption += f'{place}. {card_name}\n'
        expected_message_caption += '\n'

    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_POPULARITY_GRAPH)

    expected_update_calls = [
        mocker.call.answer(),
        mocker.call.edit_message_media(media=image),
        mocker.call.edit_message_caption(
            caption=expected_message_caption,
            reply_markup=reply_markup_keyboard
        )
    ]

    mocked_update.callback_query.assert_has_calls(expected_update_calls)


params_graph_for_gpu_func = [
    (SHOW_30_DAYS_GPU, 'PALIT GEFORCE RTX 3070 TI GAMINGPRO', 30),
    (SHOW_60_DAYS_GPU, 'GEFORCE RTX 3060 RTX3060 DUAL OC 12G', 60),
    (SHOW_90_DAYS_GPU, 'GEFORCE RTX 4080 EAGLE OC 16GB', 90)
]


@pytest.mark.bot
@pytest.mark.parametrize('graph_state, card_name, days', params_graph_for_gpu_func)
def test_graph_for_gpu_func(mocked_update_context, mocker, requests_mock,
                            graph_state, card_name, days):
    mocked_update, mocked_context = mocked_update_context
    mocked_update.callback_query.data = str(graph_state)
    mocked_context.user_data[CURRENT_GPU] = card_name
    mocked_context.user_data[CURRENT_USER_NAME] = 'Tester'

    url = f'http://173.18.0.3:8080/price?cardName={card_name}'

    with open(f'resources/graph-for-gpu-data-{card_name.replace(" ", "-")}.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    requests_mock.get(url, json=json_data)

    return_value = graph_for_gpu_func(mocked_update, mocked_context)
    assert return_value == GRAPH_SUBMENU_ON_GPU

    expected_context_calls = [
        mocker.call.__setitem__(CURRENT_GPU, card_name),
        mocker.call.__setitem__(CURRENT_USER_NAME, 'Tester'),
        mocker.call.__setitem__(CURRENT_GRAPH_GPU_DAYS, days),
        mocker.call.__getitem__(CURRENT_GRAPH_GPU_DAYS),
        mocker.call.__getitem__(CURRENT_GPU),
        mocker.call.__getitem__(CURRENT_USER_NAME),
        mocker.call.__setitem__(CURRENT_TEMP_DATA, str(graph_state))
    ]

    mocked_context.user_data.assert_has_calls(expected_context_calls)

    with open('graphic.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    expected_message_caption = f'submenu: for_gpu\n' \
                           f'gpu: {card_name}\n' \
                           f'days: {str(days)}\n' + select_graph_text

    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_GRAPH_PERIODS)

    expected_update_calls = [
        mocker.call.answer(),
        mocker.call.edit_message_media(media=image),
        mocker.call.edit_message_caption(
            caption=expected_message_caption,
            reply_markup=reply_markup_keyboard
        )
    ]

    mocked_update.callback_query.assert_has_calls(expected_update_calls)


params_draw_graph = [
    (["PALIT", "ASUS"], get_days_list(), {}, 'GEFORCE RTX 3090', 'MVIDEO', 30, 'min'),
    (["PALIT", "ASUS"], get_days_list(), {}, 'GEFORCE RTX 3090', 'DNS', 60, 'max'),
    (["PALIT", "ASUS"], get_days_list(), {}, 'GEFORCE RTX 3090', 'CITILINK', 90, 'average')
]

@pytest.mark.bot
@pytest.mark.parametrize('vendors_names, days, prices, series, shop, days_mode, graph_level', params_draw_graph)
def test_draw_graph(vendors_names, days, prices, series, shop, days_mode, graph_level, graph_offers_vendors_data):
    define_prices_by_graph_level(days, graph_level, graph_offers_vendors_data, prices, ["PALIT", "ASUS"])

    draw_graph(vendors_names, days, prices, series, shop, 'vendor', days_mode)

    expected_file = pathlib.Path(f'resources/graphic-{shop}-{days_mode}-{graph_level}.png')
    actual_file = pathlib.Path('graphic.png')
    assert filecmp.cmp(expected_file, actual_file, shallow=False) == True


@pytest.mark.bot
def test_allocate_names_and_dates():
    offer = {'cardName': 'GEFORCE GTX 3060 TI VENTUS OC', 'date': '2023-01-01', 'cardPrice': '30000'}
    offers = {}
    vendor = 'ASUS'
    allocate_names_and_dates(vendor, offer, offers)
    assert vendor in offers
    assert '2023-01-01' in offers[vendor]
    assert 'GEFORCE GTX 3060 TI VENTUS OC' in offers[vendor]['2023-01-01']
    assert '30000' == offers[vendor]['2023-01-01']['GEFORCE GTX 3060 TI VENTUS OC']
