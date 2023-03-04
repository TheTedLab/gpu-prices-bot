import ast
import datetime
import json
import colorsys
import pendulum
import matplotlib.pyplot as plt
import numpy
import requests
import telegram
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from loguru import logger
from src.bot.constants import *
from src.bot.series_vendors import series_dict, vendors_dict, shops_dict, series_buttons_dict
def set_datetime(record):
    record['extra']['datetime'] = pendulum.now('Europe/Moscow').strftime('%Y-%m-%dT%H:%M:%S')

logger.configure(patcher=set_datetime)
logger.add(
    sink='logs/bot_{time:%Y-%m-%d_%H-%M-%S}.log',
    format="{extra[datetime]} | {level} | {message}",
    enqueue=True,
    rotation='00:00'
)


def start(update: Update, context: CallbackContext) -> int:
    """Вывести сообщение и клавиатуру меню на команду '/start'"""
    reset_context(context)

    user = update.message.from_user.full_name.encode(encoding='utf-8').decode()
    context.user_data[CURRENT_USER_NAME] = user
    logger.info(f'User {user} started the conversation.')

    update.message.reply_text(
        text=hello_text + f'{user}!'
    )
    update.message.reply_text(
        text=greetings_text
    )
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)

    # Отправка сообщения с текстом и добавлением InlineKeyboard
    with open(shops_logo_dir, 'rb') as photo:
        update.message.reply_photo(
            photo=photo,
            caption=using_buttons_text,
            reply_markup=reply_markup_keyboard
        )

    # Переход в состояние MENU
    return MENU


def start_over(update: Update, context: CallbackContext) -> int:
    """Выдает тот же текст и клавиатуру, что и '/start', но не как новое сообщение"""
    user = context.user_data[CURRENT_USER_NAME]
    logger.info(f'User {user} returned to the menu.')

    reset_context(context)

    context.user_data[CURRENT_USER_NAME] = user

    update_query_message_with_keyboard(
        update=update,
        context=context,
        keyboard=keyboard_MENU,
        image_path=shops_logo_dir,
        caption_text=using_buttons_text
    )

    return MENU


def reset_context(context: CallbackContext):
    """Сбросить текущий контекст (данные пользователя) после возврата в меню"""
    context.user_data[CURRENT_SUBMENU] = ''
    context.user_data[CURRENT_SHOP] = ''
    context.user_data[CURRENT_ARCH] = ''
    context.user_data[CURRENT_VENDOR] = ''
    context.user_data[CURRENT_GPU] = ''
    context.user_data[CURRENT_GRAPH_LEVEL] = 0
    context.user_data[CURRENT_GRAPH_DAYS] = 30
    context.user_data[CURRENT_GRAPH_STATE] = 8
    context.user_data[CURRENT_GRAPH_START] = 0
    context.user_data[CURRENT_TEMP_DATA] = ''
    context.user_data[CURRENT_USER_NAME] = ''


def update_query_message_with_keyboard(update: Update, context: CallbackContext, keyboard,
                                       image_path, caption_text, current_const=CURRENT_TEMP_DATA):
    """Обновить сообщение (update) с новой клавиатурой (keyboard), изображением,
     находящимся по пути (image_path) и текстом (caption_text), сохранив контекст (context)
     в список по ключу (current_const)."""
    query = update.callback_query
    context.user_data[current_const] = query.data
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard)

    with open(image_path, 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=caption_text,
        reply_markup=reply_markup_keyboard
    )


def stats_popularity_func(update: Update, context: CallbackContext) -> int:
    """Общая для статистики и популярности функция вывода кнопок и сообщения.
    Для статистики: по магазину, по производителю, по видеокарте.
    Для популярности: по магазину и по производителю."""
    user = context.user_data[CURRENT_USER_NAME]
    if update.callback_query.data == str(STATS):
        logger.info(f'User {user} pressed the statistics button.')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_STATS,
            image_path=shops_logo_dir,
            caption_text=select_stats_text
        )

        return STATS_SUBMENU
    elif update.callback_query.data == str(POPULARITY):
        logger.info(f'User {user} pressed the popularity button.')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_POPULARITY,
            image_path=shops_logo_dir,
            caption_text=select_popularity_text
        )

        return POPULARITY_SUBMENU
    else:
        logger.warning(f'User {user} pressed incorrect button for menu!')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_MENU,
            image_path=shops_logo_dir,
            caption_text=using_buttons_text
        )

        return MENU


def for_shop_vendor_stats(update: Update, context: CallbackContext) -> int:
    """Общая для категории статистики функция вывода кнопок и сообщения.
    Для кнопки по магазину: DNS, MVIDEO, CITILINK.
    Для кнопки по производителю: кнопки производителей (ASUS, MSI, Palit и другие).
    Для кнопки по видеокарте: выделена отдельная функция (см. for_gpu)."""
    user = context.user_data[CURRENT_USER_NAME]
    if update.callback_query.data == str(FOR_SHOP):
        logger.info(f'User {user} pressed the shops button for stats.')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_SHOPS,
            image_path=shops_logo_dir,
            caption_text=select_shop_text,
            current_const=CURRENT_SUBMENU
        )

        return SHOPS_SUBMENU
    elif update.callback_query.data == str(FOR_VENDOR):
        logger.info(f'User {user} pressed the vendors button for stats.')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_VENDORS,
            image_path=shops_logo_dir,
            caption_text=select_vendor_text,
            current_const=CURRENT_SUBMENU
        )

        return VENDORS_SUBMENU
    else:
        logger.warning(f'User {user} pressed incorrect button for stats!')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_MENU,
            image_path=shops_logo_dir,
            caption_text=using_buttons_text
        )

        return MENU


def for_shop_vendor_popularity(update: Update, context: CallbackContext) -> int:
    """Общая для категории популярности функция вывода кнопок и сообщения.
    Для кнопки по магазину: DNS, MVIDEO, CITILINK.
    Для кнопки по производителю: кнопки производителей (ASUS, MSI, Palit и другие)."""
    user = context.user_data[CURRENT_USER_NAME]
    if update.callback_query.data == str(POPULARITY_FOR_SHOP):
        logger.info(f'User {user} pressed the shops button for popularity.')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_SHOPS,
            image_path=shops_logo_dir,
            caption_text=select_shop_text
        )

        return POPULARITY_SHOPS_SUBMENU
    elif update.callback_query.data == str(POPULARITY_FOR_VENDOR):
        logger.info(f'User {user} pressed the vendors button for popularity.')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_VENDORS,
            image_path=shops_logo_dir,
            caption_text=select_vendor_text
        )

        return POPULARITY_VENDORS_SUBMENU
    else:
        logger.warning(f'User {user} pressed incorrect button for stats!')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_MENU,
            image_path=shops_logo_dir,
            caption_text=using_buttons_text
        )

        return MENU


def popularity_shops_graph(update: Update, context: CallbackContext) -> int:
    """Показать график популярности видеокарт по магазину"""
    query = update.callback_query
    shop = ''
    if query.data == str(DNS_SHOP):
        shop = 'DNS'
    elif query.data == str(MVIDEO_SHOP):
        shop = 'MVIDEO'
    elif query.data == str(CITILINK_SHOP):
        shop = 'CITILINK'

    url = f'http://173.18.0.3:8080/popularity/for-shop?shopName={shop}'
    response = requests.get(url=url)
    graph_data = json.loads(response.text)

    card_names, places = define_card_names_places(graph_data)

    draw_popularity_cards_places(card_names, places, shop)

    user = context.user_data[CURRENT_USER_NAME]
    logger.info(f'User {user} chose shop {shop} for popularity graph.')

    update_query_message_with_keyboard(
        update=update,
        context=context,
        keyboard=keyboard_POPULARITY_GRAPH,
        image_path='graphic.png',
        caption_text=popularity_shop_text + shop,
    )

    return POPULARITY_SHOPS_GRAPH_SUBMENU


def draw_popularity_cards_places(card_names, places, shop):
    """Построить график популярности видеокарт (card_names) по местам (places) в магазине (shop)."""
    graph_days = get_days_list()
    days_mode = 30
    plt.set_loglevel('WARNING')
    fig = plt.figure(figsize=(23.83, 11.68), dpi=100)
    num_days = range(len(graph_days[-days_mode:]))
    line_styles = ['solid', 'dashed']
    count = 0
    for card_name in card_names:
        lines = plt.plot(
            num_days,
            places[card_name][-days_mode:],
            label=card_name,
            color=get_random_color()
        )
        lines[0].set_linestyle(line_styles[count % len(line_styles)])
        plt.gca().invert_yaxis()
        count += 1
    plt.legend(bbox_to_anchor=(0.5, -0.11), loc='upper center', ncols=4)
    plt.xlim('2022-11-20', str(datetime.date.today()))
    plt.xticks(num_days, graph_days[-days_mode:], rotation=45, ha='right')
    plt.yticks(numpy.arange(10, 0, -1))
    plt.grid(axis='x', linestyle='--')
    plt.title(f'Popularity for {shop} store', fontdict={'size': 16})
    plt.xlabel(f'Period: {days_mode} days', fontdict={'size': 14})
    plt.ylabel(f'Places', fontdict={'size': 14})
    plt.savefig('graphic.png', bbox_inches='tight')
    plt.clf()
    plt.close(fig)


def define_card_names_places(graph_data):
    """Распределить полученные данные из БД (graph_data) по именам видеокарт (card_names)
    и местам (places) для построения графика."""
    places, card_names = {}, []
    for offer in graph_data:
        if len(list(offer.keys())) > 0:
            items_length = len(list(offer.values()))
            if items_length == 10:
                for card in offer.values():
                    card_name = card['cardName']
                    if card_name not in card_names:
                        card_names.append(card_name)
                        places[card_name] = []
            elif items_length < 10:
                logger.warning('not enought items')

    for offer in graph_data:
        if len(list(offer.keys())) > 0:
            items_length = len(list(offer.values()))
            if items_length == 10:
                for name in card_names:
                    is_not_card_today = True
                    for card in offer.values():
                        card_name = card['cardName']
                        card_popularity = card['cardPopularity']
                        if card_name == name:
                            is_not_card_today = False
                            places[card_name].append(card_popularity)
                    if is_not_card_today:
                        places[name].append(numpy.NaN)
            elif items_length < 10:
                logger.warning('not enought items')

    return card_names, places


def get_random_color():
    """Получить рандомный цвет, распределенный по трём каналам RGB."""
    return colorsys.hsv_to_rgb(
        numpy.random.uniform(0.0, 1),
        numpy.random.uniform(0.2, 1),
        numpy.random.uniform(0.9, 1)
    )


def popularity_vendors_graph(update: Update, context: CallbackContext) -> int:
    """Показать график популярности видеокарт по производителю"""
    query = update.callback_query

    vendor = vendors_dict.get(int(query.data)) if query.data != '' else ''

    url = f'http://173.18.0.3:8080/popularity/for-vendor?vendorName={vendor}'
    response = requests.get(url=url)
    graph_data = json.loads(response.text)

    message_caption, popularity_places_shops = define_popularity_places_shops(graph_data, vendor)

    draw_popularity_vendors_graph(popularity_places_shops, vendor)

    user = context.user_data[CURRENT_USER_NAME]
    logger.info(f'User {user} chose vendor {vendor} for popularity graph.')

    update_query_message_with_keyboard(
        update=update,
        context=context,
        keyboard=keyboard_POPULARITY_GRAPH,
        image_path='graphic.png',
        caption_text=message_caption
    )

    return POPULARITY_VENDORS_GRAPH_SUBMENU


def define_popularity_places_shops(graph_data, vendor):
    """Распределить полученные данные из БД (graph_data) по местам в магазинах
    (popularity_places_shops), дополнительно сформировав текст к графику (message_caption),
    где используется название производителя (vendor)."""
    message_caption = popularity_vendor_text + vendor + ':\n'
    popularity_places_shops = {}
    for shop in graph_data:
        message_caption += shops_emojis_dict.get(shop) + f' {shop}\n'
        popularity_places_shops[shop] = []
        for place in ['1', '2', '3']:
            if graph_data[shop].get(place) is not None:
                card_name = graph_data[shop][place]['cardName']
                message_caption += f'{place}. {card_name}\n'
                popularity_places_shops[shop].append(card_name)
            else:
                message_caption += f'{place}. No Data\n'
                popularity_places_shops[shop].append('No Data')
        popularity_places_shops[shop].reverse()
        message_caption += '\n'
    return message_caption, popularity_places_shops


def draw_popularity_vendors_graph(popularity_places_shops, vendor):
    """Построить график популярности видеокарт производителя (vendor)
     по местам (popularity_places_shops)."""
    fig = plt.figure(figsize=(22, 6))
    rects1 = plt.bar(
        [tick + 1.0 for tick in [1.0, 2.0, 3.0]],
        [int(i) for i in ['1', '2', '3']],
        width=0.2, label='CITILINK'
    )
    rects2 = plt.bar(
        [tick + 4.0 for tick in [1.0, 2.0, 3.0]],
        [int(i) for i in ['1', '2', '3']],
        width=0.2, label='DNS'
    )
    rects3 = plt.bar(
        [tick + 7.0 for tick in [1.0, 2.0, 3.0]],
        [int(i) for i in ['1', '2', '3']],
        width=0.2, label='MVIDEO'
    )
    plt.ylim(0, 4)
    plt.xticks(
        numpy.arange(1, 12, 1),
        ['', '', 'CITILINK', '', '', 'DNS', '', '', 'MVIDEO', '', '']
    )
    plt.yticks(numpy.arange(1, 4, 1))
    plt.bar_label(rects1, popularity_places_shops['CITILINK'], padding=3)
    plt.bar_label(rects2, popularity_places_shops['DNS'], padding=3)
    plt.bar_label(rects3, popularity_places_shops['MVIDEO'], padding=3)
    plt.grid(axis='y', linestyle='--')
    plt.title(f'Popularity for {vendor}')
    plt.xlabel('Shops')
    plt.ylabel('Places')
    plt.legend(bbox_to_anchor=(0.5, -0.11), loc='upper center', ncols=3)
    plt.savefig('graphic.png', bbox_inches='tight')
    plt.clf()
    plt.close(fig)


def for_gpu(update: Update, context: CallbackContext) -> int:
    """Предложить написать название видеокарты для статистики"""
    user = context.user_data[CURRENT_USER_NAME]
    logger.info(f'User {user} pressed the gpu button for stats.')

    context.user_data[CURRENT_GRAPH_GPU_LEVEL] = 0
    context.user_data[CURRENT_GRAPH_GPU_DAYS] = 30
    context.user_data[CURRENT_GRAPH_GPU_STATE] = 16
    context.user_data[CURRENT_GRAPH_GPU_START] = 0

    update_query_message_with_keyboard(
        update=update,
        context=context,
        keyboard=keyboard_EMPTY,
        image_path=shops_logo_dir,
        caption_text=select_gpu_text
    )

    return GPU_SUBMENU


def arch_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора архитектуры видеокарты: NVIDIA, AMD и 'Другие'."""
    user = context.user_data[CURRENT_USER_NAME]
    submenu = context.user_data[CURRENT_SUBMENU]
    if submenu == str(FOR_SHOP):
        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_ARCHITECTURES,
            image_path=shops_logo_dir,
            caption_text=select_arch_text,
            current_const=CURRENT_SHOP
        )

        shop_index = context.user_data[CURRENT_SHOP]
        shop = shops_dict.get(int(shop_index)) if shop_index != '' else ''
        logger.info(f'User {user} chose shop {shop} for stats.')

        return ARCHITECTURE_SUBMENU
    elif submenu == str(FOR_VENDOR):
        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_ARCHITECTURES,
            image_path=shops_logo_dir,
            caption_text=select_arch_text,
            current_const=CURRENT_VENDOR
        )

        vendor_index = context.user_data[CURRENT_VENDOR]
        vendor = vendors_dict.get(int(vendor_index)) if vendor_index != '' else ''
        logger.info(f'User {user} chose vendor {vendor} for stats.')

        return ARCHITECTURE_SUBMENU
    else:
        logger.warning(f'User {user} chose incorrect button for stats!')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_MENU,
            image_path=shops_logo_dir,
            caption_text=using_buttons_text
        )

        return MENU


def nvidia_amd_other_func(update: Update, context: CallbackContext) -> int:
    """Общая функция для вывода кнопок выбора серии видеокарт NVIDIA, AMD, OTHER, INTEL и MATROX."""
    user = context.user_data[CURRENT_USER_NAME]
    if update.callback_query.data == str(NVIDIA):
        logger.info(f'User {user} chose NVIDIA arch for stats.')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_NVIDIA_SERIES,
            image_path=shops_logo_dir,
            caption_text=select_series_text,
            current_const=CURRENT_ARCH
        )

        return NVIDIA_SERIES_SUBMENU
    elif update.callback_query.data == str(AMD):
        logger.info(f'User {user} chose AMD arch for stats.')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_AMD_SERIES,
            image_path=shops_logo_dir,
            caption_text=select_series_text,
            current_const=CURRENT_ARCH
        )

        return AMD_SERIES_SUBMENU
    elif update.callback_query.data == str(OTHER_ARCH):
        logger.info(f'User {user} chose OTHER arch category for stats.')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_OTHER_ARCH,
            image_path=shops_logo_dir,
            caption_text=select_arch_text
        )

        return OTHER_ARCH_SUBMENU
    elif update.callback_query.data == str(INTEL):
        logger.info(f'User {user} chose INTEL arch for stats.')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_INTEL_SERIES,
            image_path=shops_logo_dir,
            caption_text=select_series_text,
            current_const=CURRENT_ARCH
        )

        return INTEL_SERIES_SUBMENU
    elif update.callback_query.data == str(MATROX):
        logger.info(f'User {user} chose MATROX arch for stats.')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_MATROX_SERIES,
            image_path=shops_logo_dir,
            caption_text=select_series_text,
            current_const=CURRENT_ARCH
        )

        return MATROX_SERIES_SUBMENU
    else:
        logger.warning(f'User {user} chose incorrect arch for stats!')

        update_query_message_with_keyboard(
            update=update,
            context=context,
            keyboard=keyboard_MENU,
            image_path=shops_logo_dir,
            caption_text=using_buttons_text
        )

        return MENU


def nvidia_series_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    user = context.user_data[CURRENT_USER_NAME]
    series_button = update.callback_query.data
    logger.info(
        f'User {user} chose '
        f'{series_buttons_dict.get(int(series_button))["name"] if series_button != "" else "incorrect name"} button.'
    )
    keyboard = series_buttons_dict.get(int(series_button))['keyboard'] if series_button != '' else keyboard_ONLY_BACK

    update_query_message_with_keyboard(
        update=update,
        context=context,
        keyboard=keyboard,
        image_path=shops_logo_dir,
        caption_text=select_series_text,
    )

    return series_buttons_dict.get(int(series_button))['returning'] if series_button != '' else MENU


def amd_series_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт AMD"""
    user = context.user_data[CURRENT_USER_NAME]
    series_button = update.callback_query.data
    logger.info(
        f'User {user} chose '
        f'{series_buttons_dict.get(int(series_button))["name"] if series_button != "" else "incorrect name"} button.'
    )
    keyboard = series_buttons_dict.get(int(series_button))['keyboard'] if series_button != '' else keyboard_ONLY_BACK

    update_query_message_with_keyboard(
        update=update,
        context=context,
        keyboard=keyboard,
        image_path=shops_logo_dir,
        caption_text=select_series_text,
    )

    return series_buttons_dict.get(int(series_button))['returning'] if series_button != '' else MENU


def graph_for_gpu_func(update: Update, context: CallbackContext) -> int:
    """Показать график цен по видеокарте"""

    submenu_title, shop_title, vendor = 'for_gpu', '', 20

    query = update.callback_query

    graph_state = query.data
    if graph_state == str(SHOW_30_DAYS_GPU):
        context.user_data[CURRENT_GRAPH_GPU_DAYS] = 30
    elif graph_state == str(SHOW_60_DAYS_GPU):
        context.user_data[CURRENT_GRAPH_GPU_DAYS] = 60
    elif graph_state == str(SHOW_90_DAYS_GPU):
        context.user_data[CURRENT_GRAPH_GPU_DAYS] = 90

    graph_days = context.user_data[CURRENT_GRAPH_GPU_DAYS]

    card_name = context.user_data[CURRENT_GPU]

    url = f'http://173.18.0.3:8080/price?cardName={card_name}'
    response = requests.get(url=url)
    graph_data = json.loads(response.text)

    offers, prices = {}, []
    days = get_days_list()

    for offer in graph_data:
        card_price = offer['cardPrice']
        date = offer['date'].split('T')[0]
        offers[date] = card_price

    define_gpu_days_prices(days, offers, prices)

    draw_gpu_graph(days, prices, card_name, days_mode=graph_days)

    user = context.user_data[CURRENT_USER_NAME]
    logger.info(f'User {user} chose gpu {card_name} for {graph_days} days stats graph.')

    caption_message_text = f'submenu: {submenu_title}\n' \
                           f'gpu: {card_name}\n' \
                           f'days: {str(graph_days)}\n' + select_graph_text

    update_query_message_with_keyboard(
        update=update,
        context=context,
        keyboard=keyboard_GRAPH_PERIODS,
        image_path='graphic.png',
        caption_text=caption_message_text
    )

    return GRAPH_SUBMENU_ON_GPU


def define_gpu_days_prices(days, offers, prices):
    """Распределить записи о видеокартах (offers) по дням (days) и ценам (prices)
    для построения графика."""
    for day in days:
        is_from_begin = True
        choosing_day = day
        while offers.get(choosing_day) is None:
            if choosing_day == '2022-11-20':
                choose_days_list = list(offers.keys())
                if len(choose_days_list) > 0:
                    choosing_day = list(offers.keys())[0]
                is_from_begin = False
                break
            date_year, date_month, date_day = [int(i) for i in choosing_day.split('-')]
            prev_day = str(
                datetime.date(
                    date_year, date_month, date_day
                ) - datetime.timedelta(days=1)
            )
            choosing_day = prev_day
        if is_from_begin:
            prices.append(offers.get(choosing_day))
        else:
            prices.append(numpy.NaN)


def draw_gpu_graph(graph_days, graph_prices, card_name, days_mode=30):
    """Построить график статистики цен на видеокарту (graph_prices) по дням (graph_days) с названием
     видеокарты (card_name) и режимом отображения (days_mode) по умолчанию 30 дней."""
    plt.set_loglevel('WARNING')
    fig = plt.figure(figsize=(23.83, 11.68), dpi=100)
    num_days = range(len(graph_days[-days_mode:]))
    plt.plot(num_days, graph_prices[-days_mode:], label=card_name)
    plt.legend(bbox_to_anchor=(0.5, -0.11), loc='upper center', ncols=4)
    plt.xlim('2022-11-20', str(datetime.date.today()))
    plt.xticks(num_days, graph_days[-days_mode:], rotation=45, ha='right')
    plt.grid(axis='x', linestyle='--')
    plt.title(f'Statistics for {card_name}', fontdict={'size': 16})
    plt.xlabel(f'Period: {days_mode} days', fontdict={'size': 14})
    plt.ylabel(f'Price, RUB', fontdict={'size': 14})
    plt.savefig('graphic.png', bbox_inches='tight')
    plt.clf()
    plt.close(fig)


def graph_func(update: Update, context: CallbackContext) -> int:
    """Показать график цен"""
    user_data = context.user_data
    submenu = user_data[CURRENT_SUBMENU]

    submenu_title, shop, vendor = '', '', 20
    if submenu == str(FOR_SHOP):
        submenu_title = 'for_shop'
        shop = user_data[CURRENT_SHOP]

        if shop == str(DNS_SHOP):
            shop = "DNS"
        elif shop == str(MVIDEO_SHOP):
            shop = "MVIDEO"
        elif shop == str(CITILINK_SHOP):
            shop = "CITILINK"
        else:
            print('unknown_shop')
    elif submenu == str(FOR_VENDOR):
        submenu_title = 'for_vendor'
        vendor = user_data[CURRENT_VENDOR]
        shop = ''
    else:
        print('unknown_submenu')

    architecture = user_data[CURRENT_ARCH]
    arch = ''
    if architecture == str(NVIDIA):
        arch = 'NVIDIA'
    elif architecture == str(AMD):
        arch = 'AMD'
    elif architecture == str(INTEL):
        arch = 'INTEL'
    elif architecture == str(MATROX):
        arch = 'MATROX'
    else:
        print('unknown architecture')

    query = update.callback_query

    if user_data[CURRENT_GRAPH_START] == 0:
        user_data[CURRENT_GRAPH_START] = 1
        graph_state = user_data[CURRENT_GRAPH_STATE]
    else:
        graph_state = query.data
        user_data[CURRENT_GRAPH_STATE] = graph_state

    series = ''
    if graph_state == str(SHOW_30_DAYS):
        series = user_data[CURRENT_SERIES]
        context.user_data[CURRENT_GRAPH_DAYS] = 30
    elif graph_state == str(SHOW_60_DAYS):
        series = user_data[CURRENT_SERIES]
        context.user_data[CURRENT_GRAPH_DAYS] = 60
    elif graph_state == str(SHOW_90_DAYS):
        series = user_data[CURRENT_SERIES]
        context.user_data[CURRENT_GRAPH_DAYS] = 90
    elif graph_state == str(GRAPH_MIN):
        series = user_data[CURRENT_SERIES]
        context.user_data[CURRENT_GRAPH_LEVEL] = 0
    elif graph_state == str(GRAPH_AVERAGE):
        series = user_data[CURRENT_SERIES]
        context.user_data[CURRENT_GRAPH_LEVEL] = 1
    elif graph_state == str(GRAPH_MAX):
        series = user_data[CURRENT_SERIES]
        context.user_data[CURRENT_GRAPH_LEVEL] = 2
    elif graph_state == 8:
        context.user_data[CURRENT_SERIES] = query.data
        series = query.data

    graph_days = context.user_data[CURRENT_GRAPH_DAYS]
    graph_level_int = context.user_data[CURRENT_GRAPH_LEVEL] + 3

    graph_level = ''
    if graph_level_int == GRAPH_MIN:
        graph_level = 'min'
    elif graph_level_int == GRAPH_AVERAGE:
        graph_level = 'average'
    elif graph_level_int == GRAPH_MAX:
        graph_level = 'max'

    vendor = vendors_dict.get(int(vendor)) if vendor != '' else ''
    series = series_dict.get(int(series)).replace(" ", "+")

    is_graph_data_empty = True
    if submenu_title == 'for_shop':
        url = f'http://173.18.0.3:8080/price/for-shop?seriesName={series}&shopName={shop}'
        response = requests.get(url=url)
        graph_data = json.loads(response.text)

        if graph_data:
            is_graph_data_empty = False
            offers, prices, vendors_names = {}, {}, []
            days = get_days_list()
            for offer in graph_data:
                card_vendor = offer['vendorName']
                if card_vendor not in vendors_names:
                    vendors_names.append(card_vendor)
                allocate_names_and_dates(card_vendor, offer, offers)

            define_prices_by_graph_level(days, graph_level, offers, prices, vendors_names)

            draw_graph(vendors_names, days, prices, series, shop, graph_mode='shop', days_mode=graph_days)
    elif submenu_title == 'for_vendor':
        url = f'http://173.18.0.3:8080/price/for-vendor?seriesName={series}&vendorName={vendor}'
        response = requests.get(url=url)
        graph_data = json.loads(response.text)

        if graph_data:
            is_graph_data_empty = False
            offers, prices, shops_names = {}, {}, ['MVIDEO', 'CITILINK', 'DNS']
            days = get_days_list()

            for shop_i in shops_names:
                offers[shop_i] = {}

            for offer in graph_data:
                shop_name = offer['shopName']
                allocate_names_and_dates(shop_name, offer, offers)

            define_prices_by_graph_level(days, graph_level, offers, prices, shops_names)

            draw_graph(shops_names, days, prices, series, vendor, graph_mode='vendor', days_mode=graph_days)
    else:
        print('unknown_submenu')

    query.answer()

    if is_graph_data_empty:
        reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ONLY_BACK)
        with open(no_search_results_dir, 'rb') as photo:
            image = telegram.InputMediaPhoto(photo)
    else:
        reply_markup_keyboard = InlineKeyboardMarkup(keyboard_GRAPH)
        with open('graphic.png', 'rb') as photo:
            image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    user = context.user_data[CURRENT_USER_NAME]
    series = series.replace('+', ' ')

    if is_graph_data_empty:
        logger.info(f'User {user} get no data for {series}.')
        query.edit_message_caption(
            caption=no_data_text,
            reply_markup=reply_markup_keyboard
        )
    else:
        logger.info(f'User {user} chose {series} button for stats graph '
                    f'with {graph_days} days and {graph_level} level.')

        query.edit_message_caption(
            caption=f'submenu: {submenu_title}\n'
                    f'shop: {shop}\n'
                    f'vendor: {vendor}\n'
                    f'arch: {arch}\n'
                    f'series: {series}\n'
                    f'days: {str(graph_days)}\n'
                    f'level: {graph_level}\n' + select_graph_text,
            reply_markup=reply_markup_keyboard
        )

    # Переход в состояние GRAPH_SUBMENU
    return GRAPH_SUBMENU


def define_prices_by_graph_level(days, graph_level, offers, prices, shops_names):
    """Передать записи о видеокартах (offers) по уровню графика (graph_level)
    для дальнейшего распределения."""
    result_mode = ''
    if graph_level == 'min':
        result_mode = define_names_days_prices(shops_names, days, offers, prices, mode='min')
    elif graph_level == 'max':
        result_mode = define_names_days_prices(shops_names, days, offers, prices, mode='max')
    elif graph_level == 'average':
        result_mode = define_names_days_prices(shops_names, days, offers, prices, mode='average')
    else:
        result_mode = graph_level
        logger.warning(f'Unknown graph level {graph_level}!')
    return result_mode


def allocate_names_and_dates(card_vendor, offer, offers):
    """Распределить запись о видеокарте (offer) по словарю записей (offers)
     с указанием производителя (card_vendor)."""
    if card_vendor not in offers:
        offers[card_vendor] = {}
    date = offer['date'].split('T')[0]
    if date not in offers[card_vendor]:
        offers[card_vendor][date] = {}
    offers[card_vendor][date][offer['cardName']] = offer['cardPrice']


def get_days_list():
    """Получить список дат всех дней, начиная со дня сбора 20.11.2022 и до сегодняшнего дня."""
    base = datetime.date(2022, 11, 20)
    now = datetime.datetime.today().date()
    days = [str(base + datetime.timedelta(days=x)) for x in range((now - base).days + 1)]
    return days


def draw_graph(vendors, days, prices, series, shop, graph_mode='shop', days_mode=30):
    """Построить график по статистики по дням (days) и ценам (prices) для имен (vendors/shops)
    с указанием серии (series), магазина (shop), режима отображения (graph_mode)
     и количества дней (days_mode)."""

    series = series.replace('+', ' ')

    plt.set_loglevel('WARNING')
    fig = plt.figure(figsize=(23.83, 11.68), dpi=100)
    num_days = range(len(days[-days_mode:]))
    for card_vendor in vendors:
        plt.plot(num_days, prices[card_vendor][-days_mode:], label=card_vendor)
    plt.legend(bbox_to_anchor=(0.5, -0.11), loc='upper center', ncols=4)
    plt.xlim('2022-11-20', str(datetime.date.today()))
    plt.xticks(num_days, days[-days_mode:], rotation=45, ha='right')
    plt.grid(axis='x', linestyle='--')
    if graph_mode == 'shop':
        plt.title(f'Statistics for {series} in {shop} store', fontdict={'size': 16})
    elif graph_mode == 'vendor':
        plt.title(f'Statistics for {shop} {series} in stores', fontdict={'size': 16})
    plt.xlabel(f'Period: {days_mode} days', fontdict={'size': 14})
    plt.ylabel(f'Price, RUB', fontdict={'size': 14})
    plt.savefig('graphic.png', bbox_inches='tight')
    plt.clf()
    plt.close(fig)


def define_names_days_prices(vendors, days, offers, prices, mode='min'):
    """Распределить записи о видеокартах (offers) по дням (days) и ценам (prices)
    с указанием имен и режима отображения (mode) по умолчанию min."""
    for card_vendor in vendors:
        prices[card_vendor] = []
        for day in days:
            is_from_begin = True
            choosing_day = day
            while offers[card_vendor].get(choosing_day) is None:
                if choosing_day == '2022-11-20':
                    choose_days_list = list(offers[card_vendor].keys())
                    if len(choose_days_list) > 0:
                        choosing_day = list(offers[card_vendor].keys())[0]
                    is_from_begin = False
                    break
                date_year, date_month, date_day = [int(i) for i in choosing_day.split('-')]
                prev_day = str(
                    datetime.date(
                        date_year, date_month, date_day
                    ) - datetime.timedelta(days=1)
                )
                choosing_day = prev_day
            if is_from_begin:
                if mode == 'min':
                    vendor = min(offers[card_vendor][choosing_day], key=offers[card_vendor][choosing_day].get)
                    prices[card_vendor].append(offers[card_vendor][choosing_day][vendor])
                elif mode == 'max':
                    vendor = max(offers[card_vendor][choosing_day], key=offers[card_vendor][choosing_day].get)
                    prices[card_vendor].append(offers[card_vendor][choosing_day][vendor])
                elif mode == 'average':
                    prices[card_vendor].append(
                        sum(offers[card_vendor][choosing_day].values()) // len(offers[card_vendor][choosing_day]))
                else:
                    print('unknown mode')
            else:
                prices[card_vendor].append(numpy.NaN)
    return mode


def help_func(update: Update, context: CallbackContext):
    """Возвращает информацию о всех командах и функциях."""
    update.message.reply_text(text=help_text)


def gpu_search_func(update: Update, context: CallbackContext) -> int:
    """Возвращает информацию поиска по конкретной видеокарте."""
    context.user_data[CURRENT_DATA] = update.message.text
    gpu_name = context.user_data[CURRENT_DATA]
    user = update.message.from_user.full_name
    logger.info(f'User {user} entered gpu name {gpu_name}.')
    gpu_search_list.clear()
    # Запрос gpu_name в БД
    url = f'http://173.18.0.3:8080/is-card-present?cardName={gpu_name}'
    response = requests.get(url=url)
    is_card_present = json.loads(response.text)

    if is_card_present:
        gpu_search_list.append(gpu_name)

    if len(gpu_search_list) != 0:
        inline_keyboard_gpu_search_buttons(gpu_search_list)
        reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_SEARCH)
        with open(search_dir, 'rb') as photo:
            update.message.reply_photo(
                photo=photo,
                caption=search_results_for_text + gpu_name + ": ",
                reply_markup=reply_markup_keyboard
            )
        # Переход в состояние ON_SEARCH
        return ON_SEARCH
    else:
        with open(no_search_results_dir, 'rb') as photo:
            update.message.reply_photo(
                photo=photo,
                caption=no_search_results_text,
                reply_markup=InlineKeyboardMarkup(keyboard_ONLY_BACK)
            )
        # Переход в состояние ON_GPU_QUESTION -> выход в меню
        return ON_GPU_QUESTION


def gpu_info(update: Update, context: CallbackContext) -> int:
    """Возвращает информацию по видеокарте."""
    query = update.callback_query
    if query.data.startswith("['gpu'"):
        gpu_index = ast.literal_eval(query.data)[1]
        gpu_name = keyboard_ON_SEARCH[int(gpu_index)][0].text
        context.user_data[CURRENT_DATA] = gpu_name
        user = context.user_data[CURRENT_USER_NAME]
        logger.info(f'User {user} chose gpu name {gpu_name}.')
        context.user_data[CURRENT_GPU] = gpu_name

        reply_markup_keyboard = InlineKeyboardMarkup(keyboard_GRAPH_PERIODS)

        with open(shops_logo_dir, 'rb') as photo:
            image = telegram.InputMediaPhoto(photo)

        query.edit_message_media(
            media=image
        )

        query.edit_message_caption(
            caption=select_graph_text,
            reply_markup=reply_markup_keyboard
        )

    # Переход в состояние GRAPH_SUBMENU_ON_GPU
    return GRAPH_SUBMENU_ON_GPU


def inline_keyboard_gpu_search_buttons(gpu_search: []):
    """Вставка кнопок в клавиатуру из найденных видеокарт (gpu_search) по запросу из БД."""
    # Получаем только уникальные видеокарты из поиска
    unique_gpu = list({gpu: gpu for gpu in gpu_search}.values())
    # Очистка клавиатуры
    keyboard_ON_SEARCH.clear()
    for gpu in unique_gpu:
        keyboard_ON_SEARCH.append(
            [InlineKeyboardButton(
                gpu, callback_data="['gpu', '" + str(unique_gpu.index(gpu)) + "']"
            )]
        )


def end_on_gpu(update: Update, context: CallbackContext) -> int:
    """Конец разговора по видеокарте, возврат к основному разговору."""
    user = context.user_data[CURRENT_USER_NAME]
    logger.info(f'User {user} ended for gpu searching.')
    new_start(update, context)
    return BACK_TO_MENU


def start_fallback(update, context) -> int:
    """Функция обертка для start, чтобы сделать fallback
     по нажатию /start в любом состоянии разговора."""
    start(update, context)
    return BACK_TO_MENU


def error_attention(update: Update, context: CallbackContext):
    """Вывод сообщения об ошибке, если пользователь ввел текст не выбирая кнопок."""
    user = update.message.from_user.full_name.encode(encoding='utf-8').decode()
    logger.info(f'User {user} entered message without a reason.')

    update.message.reply_text(
        text=error_enter_text
    )


def new_start(update: Update, context: CallbackContext):
    """Возвращает текст и клавиатуру к главному меню."""
    user = context.user_data[CURRENT_USER_NAME]
    logger.info(f'User {user} returned to the menu.')

    update_query_message_with_keyboard(
        update=update,
        context=context,
        keyboard=keyboard_MENU,
        image_path=shops_logo_dir,
        caption_text=using_buttons_text,
    )

    return MENU
