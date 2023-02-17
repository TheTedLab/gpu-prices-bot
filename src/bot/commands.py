import ast
import datetime
import json
import logging
import colorsys

import matplotlib.pyplot as plt
import numpy
import requests
import telegram
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from constants import *
from series_vendors import series_dict, vendors_dict

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> int:
    """Отправить сообщение на `/start`."""
    context.user_data[CURRENT_SUBMENU] = ''
    context.user_data[CURRENT_SHOP] = ''
    context.user_data[CURRENT_ARCH] = ''
    context.user_data[CURRENT_VENDOR] = ''
    context.user_data[CURRENT_GPU] = ''
    context.user_data[CURRENT_GRAPH_LEVEL] = 0
    context.user_data[CURRENT_GRAPH_DAYS] = 30
    context.user_data[CURRENT_GRAPH_STATE] = 8
    context.user_data[CURRENT_GRAPH_START] = 0
    user = update.message.from_user.full_name
    logger.info("User <%s> started the conversation.", user)
    update.message.reply_text(
        hand_emoji + fr'Привет, {user}!'
    )
    update.message.reply_text(greetings_text)
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)
    # Отправка сообщения с текстом и добавлением InlineKeyboard

    with open('images/shops_logo.jpg', 'rb') as photo:
        update.message.reply_photo(
            photo=photo,
            caption=using_buttons_text,
            reply_markup=reply_markup_keyboard
        )

    # Переход в состояние MENU
    return MENU


def start_over(update: Update, context: CallbackContext) -> int:
    """Выдает тот же текст и клавиатуру, что и `start`, но не как новое сообщение"""
    context.user_data[CURRENT_SUBMENU] = ''
    context.user_data[CURRENT_SHOP] = ''
    context.user_data[CURRENT_ARCH] = ''
    context.user_data[CURRENT_VENDOR] = ''
    context.user_data[CURRENT_GPU] = ''
    context.user_data[CURRENT_GRAPH_LEVEL] = 0
    context.user_data[CURRENT_GRAPH_DAYS] = 30
    context.user_data[CURRENT_GRAPH_STATE] = 8
    context.user_data[CURRENT_GRAPH_START] = 0

    # Получить запрос обратного вызова из обновления
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)
    # Вместо отправки нового сообщения редактируем сообщение, которое
    # породило запрос обратного вызова.

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=using_buttons_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние MENU
    return MENU


def stats(update: Update, context: CallbackContext) -> int:
    """Показать кнопки статистики цен видеокарт"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_STATS)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_stats_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние STATS_SUBMENU
    return STATS_SUBMENU


def popularity(update: Update, context: CallbackContext) -> int:
    """Показать кнопки популярности видеокарт"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_POPULARITY)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_popularity_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние POPULARITY_SUBMENU
    return POPULARITY_SUBMENU


def for_shop_popularity(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_SHOPS)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_shop_text,
        reply_markup=reply_markup_keyboard
    )

    return POPULARITY_SHOPS_SUBMENU


def for_vendor_popularity(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_VENDORS)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_vendor_text,
        reply_markup=reply_markup_keyboard
    )

    return POPULARITY_VENDORS_SUBMENU


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

    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_POPULARITY_GRAPH)

    with open('graphic.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=f'Популярность по магазину {shop}',
        reply_markup=reply_markup_keyboard
    )

    return POPULARITY_SHOPS_GRAPH_SUBMENU


def draw_popularity_cards_places(card_names, places, shop):
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
                print('not enough items')

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
                print('not enough items')

    return card_names, places


def get_random_color():
    return colorsys.hsv_to_rgb(
        numpy.random.uniform(0.0, 1),
        numpy.random.uniform(0.2, 1),
        numpy.random.uniform(0.9, 1)
    )


def popularity_vendors_graph(update: Update, context: CallbackContext) -> int:
    query = update.callback_query

    vendor = ''
    if query.data == str(VENDOR_AFOX):
        vendor = 'AFOX'
    elif query.data == str(VENDOR_ASROCK):
        vendor = 'ASROCK'
    elif query.data == str(VENDOR_ASUS):
        vendor = 'ASUS'
    elif query.data == str(VENDOR_BIOSTAR):
        vendor = 'BIOSTAR'
    elif query.data == str(VENDOR_COLORFUL):
        vendor = 'COLORFUL'
    elif query.data == str(VENDOR_DELL):
        vendor = 'DELL'
    elif query.data == str(VENDOR_EVGA):
        vendor = 'EVGA'
    elif query.data == str(VENDOR_GIGABYTE):
        vendor = 'GIGABYTE'
    elif query.data == str(VENDOR_INNO3D):
        vendor = 'INNO3D'
    elif query.data == str(VENDOR_KFA2):
        vendor = 'KFA2'
    elif query.data == str(VENDOR_MATROX):
        vendor = 'MATROX'
    elif query.data == str(VENDOR_MSI):
        vendor = 'MSI'
    elif query.data == str(VENDOR_NVIDIA):
        vendor = 'NVIDIA'
    elif query.data == str(VENDOR_PALIT):
        vendor = 'PALIT'
    elif query.data == str(VENDOR_PNY):
        vendor = 'PNY'
    elif query.data == str(VENDOR_POWERCOLOR):
        vendor = 'POWERCOLOR'
    elif query.data == str(VENDOR_SAPPHIRE):
        vendor = 'SAPPHIRE'
    elif query.data == str(VENDOR_SINOTEX):
        vendor = 'SINOTEX'
    elif query.data == str(VENDOR_XFX):
        vendor = 'XFX'
    elif query.data == str(VENDOR_ZOTAC):
        vendor = 'ZOTAC'

    url = f'http://173.18.0.3:8080/popularity/for-vendor?vendorName={vendor}'
    response = requests.get(url=url)
    graph_data = json.loads(response.text)

    places = ['1', '2', '3']

    message_caption = f'Популярность по производителю {vendor}:\n'

    popularity_places_shops = {}
    for shop in graph_data:
        message_caption += shops_emojis_dict.get(shop) + f' {shop}\n'
        popularity_places_shops[shop] = []
        for place in places:
            if graph_data[shop].get(place) is not None:
                card_name = graph_data[shop][place]['cardName']
                message_caption += f'{place}. {card_name}\n'
                popularity_places_shops[shop].append(card_name)
            else:
                message_caption += f'{place}. No Data\n'
                popularity_places_shops[shop].append('No Data')
        popularity_places_shops[shop].reverse()
        message_caption += '\n'

    x = [1.0, 2.0, 3.0]

    fig = plt.figure(figsize=(22, 6))

    rects1 = plt.bar([tick + 1.0 for tick in x], [int(i) for i in places], width=0.2, label='CITILINK')
    rects2 = plt.bar([tick + 4.0 for tick in x], [int(i) for i in places], width=0.2, label='DNS')
    rects3 = plt.bar([tick + 7.0 for tick in x], [int(i) for i in places], width=0.2, label='MVIDEO')

    plt.ylim(0, 4)
    plt.xticks(numpy.arange(1, 12, 1), ['', '', 'CITILINK', '', '', 'DNS', '', '', 'MVIDEO', '', ''])
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

    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_POPULARITY_GRAPH)

    with open('graphic.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=message_caption,
        reply_markup=reply_markup_keyboard
    )

    return POPULARITY_VENDORS_GRAPH_SUBMENU


def for_shop(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора магазина для статистики"""
    query = update.callback_query
    context.user_data[CURRENT_SUBMENU] = query.data
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_SHOPS)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_shop_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние SHOPS_SUBMENU
    return SHOPS_SUBMENU


def for_vendor(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора производителя для статистики"""
    query = update.callback_query
    context.user_data[CURRENT_SUBMENU] = query.data
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_VENDORS)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_vendor_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние VENDORS_SUBMENU
    return VENDORS_SUBMENU


def for_gpu(update: Update, context: CallbackContext) -> int:
    """Предложить написать название видеокарты для статистики"""
    user_data = context.user_data
    context.user_data[CURRENT_GRAPH_GPU_LEVEL] = 0
    context.user_data[CURRENT_GRAPH_GPU_DAYS] = 30
    context.user_data[CURRENT_GRAPH_GPU_STATE] = 16
    context.user_data[CURRENT_GRAPH_GPU_START] = 0

    query = update.callback_query
    context.user_data[CURRENT_DATA] = query.data
    query.answer()

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_gpu_text,
    )

    # Переход в состояние GPU_SUBMENU
    return GPU_SUBMENU


def arch_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора архитектуры видеокарты"""
    query = update.callback_query
    submenu = context.user_data[CURRENT_SUBMENU]
    if submenu == str(FOR_SHOP):
        context.user_data[CURRENT_SHOP] = query.data
    elif submenu == str(FOR_VENDOR):
        context.user_data[CURRENT_VENDOR] = query.data
    elif submenu == str(FOR_GPU):
        context.user_data[CURRENT_GPU] = query.data
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ARCHITECTURES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_arch_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние ARCHITECTURE_SUBMENU
    return ARCHITECTURE_SUBMENU


def nvidia_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    context.user_data[CURRENT_ARCH] = query.data
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_SERIES_SUBMENU
    return NVIDIA_SERIES_SUBMENU


def nvidia_other_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_OTHER_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_OTHER_SUBMENU
    return NVIDIA_OTHER_SUBMENU


def nvidia_quadro_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_QUADRO_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_QUADRO_SERIES_SUBMENU
    return NVIDIA_QUADRO_SERIES_SUBMENU


def quadro_AXXXX(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_QUADRO_RTX_AXXXX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_QUADRO_RTX_AXXXX_SERIES_SUBMENU
    return NVIDIA_QUADRO_RTX_AXXXX_SERIES_SUBMENU


def nvidia_tesla_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_TESLA_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_TESLA_SERIES_SUBMENU
    return NVIDIA_TESLA_SERIES_SUBMENU


def nvidia_10XX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_10XX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_10XX_SERIES_SUBMENU
    return NVIDIA_10XX_SERIES_SUBMENU


def nvidia_16XX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_16XX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_16XX_SERIES_SUBMENU
    return NVIDIA_16XX_SERIES_SUBMENU


def nvidia_1660X_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_1660X_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_1660X_SERIES_SUBMENU
    return NVIDIA_1660X_SERIES_SUBMENU


def nvidia_1650X_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_1650X_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_1650X_SERIES_SUBMENU
    return NVIDIA_1650X_SERIES_SUBMENU


def nvidia_20XX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_20XX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_20XX_SERIES_SUBMENU
    return NVIDIA_20XX_SERIES_SUBMENU


def nvidia_2060X_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_2060X_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_2060X_SERIES_SUBMENU
    return NVIDIA_2060X_SERIES_SUBMENU


def nvidia_2080X_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_2080X_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_2080X_SERIES_SUBMENU
    return NVIDIA_2080X_SERIES_SUBMENU


def nvidia_30XX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_30XX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_30XX_SERIES_SUBMENU
    return NVIDIA_30XX_SERIES_SUBMENU


def nvidia_3060X_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_3060X_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_3060X_SERIES_SUBMENU
    return NVIDIA_3060X_SERIES_SUBMENU


def nvidia_3070X_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_3070X_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_3070X_SERIES_SUBMENU
    return NVIDIA_3070X_SERIES_SUBMENU


def nvidia_3080X_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_3080X_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_3080X_SERIES_SUBMENU
    return NVIDIA_3080X_SERIES_SUBMENU


def nvidia_3090X_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_3090X_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_3090X_SERIES_SUBMENU
    return NVIDIA_3090X_SERIES_SUBMENU


def nvidia_40XX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт NVIDIA"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_NVIDIA_40XX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние NVIDIA_40XX_SERIES_SUBMENU
    return NVIDIA_40XX_SERIES_SUBMENU


def amd_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт AMD"""
    query = update.callback_query
    context.user_data[CURRENT_ARCH] = query.data
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_AMD_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние AMD_SERIES_SUBMENU
    return AMD_SERIES_SUBMENU


def amd_other_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт AMD"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_AMD_OTHER_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние AMD_OTHER_SUBMENU
    return AMD_OTHER_SUBMENU


def amd_rx_5XX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт AMD"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_AMD_RX_5XX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние AMD_RX_5XX_SERIES_SUBMENU
    return AMD_RX_5XX_SERIES_SUBMENU


def amd_rx_5XXX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт AMD"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_AMD_RX_5XXX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние AMD_RX_5XXX_SERIES_SUBMENU
    return AMD_RX_5XXX_SERIES_SUBMENU


def amd_rx_6XXX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт AMD"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_AMD_RX_6XXX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние AMD_RX_6XXX_SERIES_SUBMENU
    return AMD_RX_6XXX_SERIES_SUBMENU


def amd_rx_66XX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт AMD"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_AMD_RX_66XX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние AMD_RX_66XX_SERIES_SUBMEN
    return AMD_RX_66XX_SERIES_SUBMENU


def amd_rx_67XX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт AMD"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_AMD_RX_67XX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние AMD_RX_67XX_SERIES_SUBMENU
    return AMD_RX_67XX_SERIES_SUBMENU


def amd_rx_68XX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт AMD"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_AMD_RX_68XX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние AMD_RX_68XX_SERIES_SUBMENU
    return AMD_RX_68XX_SERIES_SUBMENU


def amd_rx_69XX_series(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт AMD"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_AMD_RX_69XX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние AMD_RX_69XX_SERIES_SUBMENU
    return AMD_RX_69XX_SERIES_SUBMENU


def other_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт AMD"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_OTHER_ARCH)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_arch_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние OTHER_ARCH_SUBMENU
    return OTHER_ARCH_SUBMENU


def intel_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт INTEL"""
    query = update.callback_query
    context.user_data[CURRENT_ARCH] = query.data
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_INTEL_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние INTEL_SERIES_SUBMENU
    return INTEL_SERIES_SUBMENU


def matrox_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора серии видеокарт MATROX"""
    query = update.callback_query
    context.user_data[CURRENT_ARCH] = query.data
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MATROX_SERIES)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=select_series_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние MATROX_SERIES_SUBMENU
    return MATROX_SERIES_SUBMENU


def graph_for_gpu_func(update: Update, context: CallbackContext) -> int:
    """Показать график цен по видеокарте"""
    user_data = context.user_data

    submenu_title, shop_title, vendor = 'for_gpu', '', 20

    query = update.callback_query

    graph_state = query.data
    if graph_state == str(SHOW_30_DAYS_GPU):
        context.user_data[CURRENT_GRAPH_GPU_DAYS] = 30
    elif graph_state == str(SHOW_60_DAYS_GPU):
        context.user_data[CURRENT_GRAPH_GPU_DAYS] = 60
    elif graph_state == str(SHOW_90_DAYS_GPU):
        context.user_data[CURRENT_GRAPH_GPU_DAYS] = 90
    elif graph_state == str(GRAPH_MIN_GPU):
        context.user_data[CURRENT_GRAPH_GPU_LEVEL] = 0
    elif graph_state == str(GRAPH_AVERAGE_GPU):
        context.user_data[CURRENT_GRAPH_GPU_LEVEL] = 1
    elif graph_state == str(GRAPH_MAX_GPU):
        context.user_data[CURRENT_GRAPH_GPU_LEVEL] = 2
    elif graph_state == 16:
        context.user_data[CURRENT_SERIES] = query.data

    graph_days = context.user_data[CURRENT_GRAPH_GPU_DAYS]
    graph_level_int = context.user_data[CURRENT_GRAPH_GPU_LEVEL] + 13

    graph_level = ''
    if graph_level_int == GRAPH_MIN_GPU:
        graph_level = 'min'
    elif graph_level_int == GRAPH_AVERAGE_GPU:
        graph_level = 'average'
    elif graph_level_int == GRAPH_MAX_GPU:
        graph_level = 'max'

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

    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_GRAPH_PERIODS)

    with open('graphic.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=f'submenu: {submenu_title}\n'
                f'gpu: {card_name}\n'
                f'days: {str(graph_days)}\n' + select_graph_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние GRAPH_SUBMENU_ON_GPU
    return GRAPH_SUBMENU_ON_GPU


def define_gpu_days_prices(days, offers, prices):
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

            for shop in shops_names:
                offers[shop] = {}

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
        with open('images/no_search_results.png', 'rb') as photo:
            image = telegram.InputMediaPhoto(photo)
    else:
        reply_markup_keyboard = InlineKeyboardMarkup(keyboard_GRAPH)
        with open('graphic.png', 'rb') as photo:
            image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    if is_graph_data_empty:
        query.edit_message_caption(
            caption=no_data_text,
            reply_markup=reply_markup_keyboard
        )
    else:
        series = series.replace('+', ' ')

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
    if graph_level == 'min':
        define_names_days_prices(shops_names, days, offers, prices, mode='min')
    elif graph_level == 'max':
        define_names_days_prices(shops_names, days, offers, prices, mode='max')
    elif graph_level == 'average':
        define_names_days_prices(shops_names, days, offers, prices, mode='average')
    else:
        print('unknown graph level')


def allocate_names_and_dates(card_vendor, offer, offers):
    if card_vendor not in offers:
        offers[card_vendor] = {}
    date = offer['date'].split('T')[0]
    if date not in offers[card_vendor]:
        offers[card_vendor][date] = {}
    offers[card_vendor][date][offer['cardName']] = offer['cardPrice']


def get_days_list():
    base = datetime.date(2022, 11, 20)
    now = datetime.datetime.today().date()
    days = [str(base + datetime.timedelta(days=x)) for x in range((now - base).days + 1)]
    return days


def draw_graph(vendors, days, prices, series, shop, graph_mode='shop', days_mode=30):

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


def help_func(update: Update, context: CallbackContext):
    """Возвращает информацию о всех командах и функциях"""
    update.message.reply_text(text=help_text)


def gpu_search_func(update: Update, context: CallbackContext) -> int:
    """Возвращает информацию поиска по конкретной видеокарте"""
    user_data = context.user_data
    user_data[CURRENT_DATA] = update.message.text
    gpu_name = user_data[CURRENT_DATA]
    user = update.message.from_user.full_name
    logger.info("User <%s> entered <%s>.", user, gpu_name)
    gpu_search_list.clear()
    # Запрос gpu_name в БД
    url = f'http://173.18.0.3:8080/is-card-present?cardName={gpu_name}'
    response = requests.get(url=url)
    is_card_present = json.loads(response.text)

    if is_card_present:
        gpu_search_list.append(gpu_name)

    if len(gpu_search_list) != 0:
        gpu_search_list.reverse()
        inline_keyboard_gpu_search_buttons(gpu_search_list)
        reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_SEARCH)
        with open('images/search.png', 'rb') as photo:
            update.message.reply_photo(
                photo=photo,
                caption="Результаты поиска для " + gpu_name + ": ",
                reply_markup=reply_markup_keyboard
            )
        # Переход в состояние ON_SEARCH
        return ON_SEARCH
    else:
        with open('images/no_search_results.png', 'rb') as photo:
            update.message.reply_photo(
                photo=photo,
                caption="Нет результатов поиска",
                reply_markup=InlineKeyboardMarkup(keyboard_ONLY_BACK)
            )
        # Переход в состояние ON_GPU_QUESTION -> выход в меню
        return ON_GPU_QUESTION


def gpu_info(update: Update, context: CallbackContext) -> int:
    """Возвращает информацию по видеокарте"""
    user_data = context.user_data
    call = update.callback_query
    if call.data.startswith("['gpu'"):
        gpu_index = ast.literal_eval(call.data)[1]
        buttons = InlineKeyboardMarkup(keyboard_ON_SEARCH).to_dict()
        buttons_list = buttons["inline_keyboard"]
        buttons_list.reverse()
        gpu_name = buttons["inline_keyboard"][int(gpu_index)][0]["text"]
        user_data[CURRENT_DATA] = gpu_name
        logger.info("User chose gpu <%s>.", gpu_name)
        context.user_data[CURRENT_GPU] = gpu_name

        reply_markup_keyboard = InlineKeyboardMarkup(keyboard_GRAPH_PERIODS)

        with open('images/shops_logo.jpg', 'rb') as photo:
            image = telegram.InputMediaPhoto(photo)

        call.edit_message_media(
            media=image
        )

        call.edit_message_caption(
            caption=select_graph_text,
            reply_markup=reply_markup_keyboard
        )

    # Переход в состояние GRAPH_SUBMENU_ON_GPU
    return GRAPH_SUBMENU_ON_GPU


def gpu_again(update: Update, context: CallbackContext) -> int:
    """Возвращает информацию по видеокарте при повторном вызове"""
    user_data = context.user_data
    query = update.callback_query
    query.answer()
    gpu_name = user_data[CURRENT_DATA]
    logger.info("User chose gpu <%s>.", gpu_name)
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GPU)

    with open('images/search.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption="Платформы для " + gpu_name + ": ",
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние ON_GPU
    return ON_GPU


def inline_keyboard_gpu_search_buttons(gpu_search: []):
    # Получаем только уникальные видеокарты из поиска
    unique_gpu = list({gpu: gpu for gpu in gpu_search}.values())
    # Очистка клавиатуры
    keyboard_ON_SEARCH.clear()
    for gpu in unique_gpu:
        keyboard_ON_SEARCH.insert(
            0,
            [InlineKeyboardButton(
                gpu, callback_data="['gpu', '" + str(unique_gpu.index(gpu)) + "']"
            )]
        )


def end_on_gpu(update: Update, context: CallbackContext) -> int:
    """Конец разговора по видеокарте, возврат к основному разговору"""
    new_start(update, context)
    return BACK_TO_MENU


def start_fallback(update, context) -> int:
    start(update, context)
    return BACK_TO_MENU


def error_attention(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Ошибка! Необходимо выбрать кнопку'
    )


def new_start(update: Update, context: CallbackContext):
    """Возвращает текст и клавиатуру к главному меню"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=using_buttons_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние MENU
    return MENU
