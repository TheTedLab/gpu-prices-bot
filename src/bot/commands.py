import ast
import logging
import requests
import json
import matplotlib.pyplot as plt

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
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_POPULARITY_GRAPH)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption='Популярность по магазину',
        reply_markup=reply_markup_keyboard
    )

    return POPULARITY_SHOPS_GRAPH_SUBMENU


def popularity_vendors_graph(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_POPULARITY_GRAPH)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption='Популярность по производителю',
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

    print('graph_for_gpu')

    submenu_title, shop_title, vendor = 'for_gpu', '', 20

    query = update.callback_query

    graph_state = query.data
    print('graph_state:', graph_state)
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
    print(graph_level_int)
    graph_level = ''
    if graph_level_int == GRAPH_MIN_GPU:
        graph_level = 'min'
    elif graph_level_int == GRAPH_AVERAGE_GPU:
        graph_level = 'average'
    elif graph_level_int == GRAPH_MAX_GPU:
        graph_level = 'max'

    print('graph days:', graph_days)
    print('graph level:', graph_level)

    gpu_name = context.user_data[CURRENT_GPU]

    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_GRAPH_GPU)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=f'submenu: {submenu_title}\n'
                f'gpu: {gpu_name}\n'
                f'days: {str(graph_days)}\n'
                f'level: {graph_level}\n' + select_graph_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние GRAPH_SUBMENU_ON_GPU
    return GRAPH_SUBMENU_ON_GPU


def graph_func(update: Update, context: CallbackContext) -> int:
    """Показать график цен"""
    user_data = context.user_data
    submenu = user_data[CURRENT_SUBMENU]

    submenu_title, shop_title, vendor = '', '', 20
    if submenu == str(FOR_SHOP):
        print('submenu: for_shop')
        submenu_title = 'for_shop'
        shop = user_data[CURRENT_SHOP]

        if shop == str(DNS_SHOP):
            print('shop: dns')
            shop_title = "DNS"
        elif shop == str(MVIDEO_SHOP):
            print('shop: mvideo')
            shop_title = "MVIDEO"
        elif shop == str(CITILINK_SHOP):
            print('shop: citilink')
            shop_title = "CITILINK"
        else:
            print('unknown_shop')
    elif submenu == str(FOR_VENDOR):
        print('submenu: for_vendor')
        submenu_title = 'for_vendor'
        vendor = user_data[CURRENT_VENDOR]
        print(vendor)

        if vendor == str(VENDOR_AFOX):
            print('vendor: AFOX')
        elif vendor == str(VENDOR_ASROCK):
            print('vendor: ASROCK')
        elif vendor == str(VENDOR_ASUS):
            print('vendor: ASUS')
        elif vendor == str(VENDOR_BIOSTAR):
            print('vendor: BIOSTAR')
        elif vendor == str(VENDOR_COLORFUL):
            print('vendor: COLORFUL')
        elif vendor == str(VENDOR_DELL):
            print('vendor: DELL')
        elif vendor == str(VENDOR_EVGA):
            print('vendor: EVGA')
        elif vendor == str(VENDOR_GIGABYTE):
            print('vendor: GIGABYTE')
        elif vendor == str(VENDOR_INNO3D):
            print('vendor: INNO3D')
        elif vendor == str(VENDOR_KFA2):
            print('vendor: KFA2')
        elif vendor == str(VENDOR_MATROX):
            print('vendor: MATROX')
        elif vendor == str(VENDOR_MSI):
            print('vendor: MSI')
        elif vendor == str(VENDOR_NVIDIA):
            print('vendor: NVIDIA')
        elif vendor == str(VENDOR_PALIT):
            print('vendor: PALIT')
        elif vendor == str(VENDOR_PNY):
            print('vendor: PNY')
        elif vendor == str(VENDOR_POWERCOLOR):
            print('vendor: POWERCOLOR')
        elif vendor == str(VENDOR_SAPPHIRE):
            print('vendor: SAPPHIRE')
        elif vendor == str(VENDOR_SINOTEX):
            print('vendor: SINOTEX')
        elif vendor == str(VENDOR_XFX):
            print('vendor: XFX')
        elif vendor == str(VENDOR_ZOTAC):
            print('vendor: ZOTAC')
    elif submenu == str(FOR_GPU):
        submenu_title = 'for_gpu'
        print('submenu: for_gpu')
    else:
        print('unknown_submenu')

    architecture = user_data[CURRENT_ARCH]

    if architecture == str(NVIDIA):
        print('architecture: nvidia')
    elif architecture == str(AMD):
        print('architecture: amd')
    elif architecture == str(INTEL):
        print('architecture: intel')
    elif architecture == str(MATROX):
        print('architecture: matrox')
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
    print('graph_state:', graph_state)
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

    print('series:', series)
    print('graph days:', graph_days)
    print('graph level:', graph_level)

    if series == str(NVIDIA_10XX_SERIES):
        print('series: GeForce 10XX')
    elif series == str(NVIDIA_16XX_SERIES):
        print('series: GeForce 16XX')
    elif series == str(NVIDIA_20XX_SERIES):
        print('series: GeForce 20XX')
    elif series == str(NVIDIA_30XX_SERIES):
        print('series: GeForce 30XX')
    elif series == str(NVIDIA_40XX_SERIES):
        print('series: GeForce 40XX')
    elif series == str(NVIDIA_QUADRO_SERIES):
        print('series: Nvidia Quadro')
    elif series == str(NVIDIA_TESLA_SERIES):
        print('series: Nvidia Tesla')
    elif series == str(NVIDIA_GT_710_SERIES):
        print('series: Nvidia GT 710')
    elif series == str(NVIDIA_GT_730_SERIES):
        print('series: Nvidia GT 730')
    elif series == str(NVIDIA_210_SERIES):
        print('series: Nvidia 210')
    elif series == str(AMD_RX5XX_SERIES):
        print('series: Radeon RX 5XX')
    elif series == str(AMD_RX5XXX_SERIES):
        print('series: Radeon RX 5XXX')
    elif series == str(AMD_RX6XXX_SERIES):
        print('series: Radeon RX 6XXX')
    elif series == str(AMD_R7_240_SERIES):
        print('series: Radeon R7 240')
    elif series == str(ARC_A310_SERIES):
        print('series: Intel Arc A310')
    elif series == str(ARC_A380_SERIES):
        print('series: Intel Arc A380')
    elif series == str(MATROX_M9120_SERIES):
        print('series: Matrox M9120')

    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_GRAPH)

    with open('images/shops_logo.jpg', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    shop = shop_title
    vendor = vendors_dict.get(int(vendor)) if vendor != '' else ''
    series = series_dict.get(int(series)).replace(" ", "+")

    if vendor == "":
        url = f'http://173.18.0.3:8080/price/for-shop?seriesName={series}&shopName={shop}'
        response = requests.get(url=url)
        listik = json.loads(response.text)

        card_names = []
        offers = {}
        prices = {}
        days = []
        for offer in listik:
            card_name = offer['cardName']
            if not card_name in offers:
                offers[card_name]={}
            date = offer['date'].split('T')[0]
            if not date in days:
                days.append(date)
            if not date in offers[card_name]:
                offers[card_name][date] = {}
            offers[card_name][date][offer['vendorName']] = offer['cardPrice']
            if not card_name in card_names:
                card_names.append(card_name)

        if graph_level == 'min':
            for card_name in card_names:
                prices[card_name] = []
                for day in days:
                    vendor = min(offers[card_name][day], key=offers[card_name][day].get)
                    prices[card_name].append(offers[card_name][day][vendor])
        elif graph_level == 'max':
            for card_name in card_names:
                prices[card_name] = []
                for day in days:
                    vendor = max(offers[card_name][day], key=offers[card_name][day].get)
                    prices[card_name].append(offers[card_name][day][vendor])
        else:
            for card_name in card_names:
                prices[card_name] = []
                for day in days:
                    prices[card_name].append(sum(offers[card_name][day].values()) // len(offers[card_name][day]))



        for card_name in card_names:
            plt.plot(days, prices[card_name], label=card_name)
        plt.legend()
        plt.xticks(rotation=45, ha='right')
        plt.savefig('graphic.png')
        plt.clf()
    else:
        url = f'http://173.18.0.3:8080/price/for-vendor?seriesName={series}&vendorName={vendor}'
        response = requests.get(url=url)
        listik = json.loads(response.text)

        vendor_names = []
        offers = {}
        prices = {}
        days = []
        for offer in listik:
            vendor_name = offer['vendorName']
            if not vendor_name in offers:
                offers[vendor_name]={}
            date = offer['date'].split('T')[0]
            if not date in days:
                days.append(date)
            if not date in offers[vendor_name]:
                offers[vendor_name][date] = {}
            offers[vendor_name][date][offer['cardName']] = offer['cardPrice']
            if not vendor_name in vendor_names:
                vendor_names.append(vendor_name)

        if graph_level == 'min':
            for vendor_name in vendor_names:
                prices[vendor_name] = []
                for day in days:
                    vendor = min(offers[vendor_name][day], key=offers[vendor_name][day].get)
                    prices[vendor_name].append(offers[vendor_name][day][vendor])
        elif graph_level == 'max':
            for vendor_name in vendor_names:
                prices[vendor_name] = []
                for day in days:
                    vendor = max(offers[vendor_name][day], key=offers[vendor_name][day].get)
                    prices[vendor_name].append(offers[vendor_name][day][vendor])
        else:
            for vendor_name in vendor_names:
                prices[vendor_name] = []
                for day in days:
                    prices[vendor_name].append(sum(offers[vendor_name][day].values()) // len(offers[vendor_name][day]))

        for vendor_name in vendor_names:
            plt.plot(days, prices[vendor_name], label=vendor_name)
        plt.legend()
        plt.xticks(rotation=45, ha='right')
        plt.savefig('graphic.png')
        plt.clf()

    with open('graphic.png', 'rb') as photo:
        image = telegram.InputMediaPhoto(photo)

    query.edit_message_media(
        media=image
    )

    query.edit_message_caption(
        caption=f'submenu: {submenu_title}\n'
                f'shop: {shop_title}\n'
                f'vendor: {vendor}\n'
                f'series: {series}\n'
                f'days: {str(graph_days)}\n'
                f'level: {graph_level}\n' + select_graph_text,
        reply_markup=reply_markup_keyboard
    )

    # Переход в состояние GRAPH_SUBMENU
    return GRAPH_SUBMENU


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

        reply_markup_keyboard = InlineKeyboardMarkup(keyboard_GRAPH_GPU)

        with open('images/shops_logo.jpg', 'rb') as photo:
            image = telegram.InputMediaPhoto(photo)

        call.edit_message_media(
            media=image
        )

        call.edit_message_caption(
            caption=gpu_name,
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
