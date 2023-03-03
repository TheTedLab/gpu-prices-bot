import pytest
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
