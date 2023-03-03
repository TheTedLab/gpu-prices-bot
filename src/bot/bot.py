from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler, Filters,
)

from src.bot.autorization import token
from src.bot.commands import *
from src.bot.constants import *


def main() -> None:
    """Start the bot."""
    # Создание Updater и связывание с токеном бота
    updater = Updater(token)

    # Получение dispatcher и регистрация handlers
    dispatcher = updater.dispatcher

    for_gpu_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(for_gpu, pattern='^' + str(FOR_GPU) + '$'),],
        states={
            ON_SEARCH: [
                CallbackQueryHandler(gpu_info, pattern=Filters.text),
            ],
            GRAPH_SUBMENU_ON_GPU: [
                CallbackQueryHandler(graph_for_gpu_func, pattern='^' + str(SHOW_30_DAYS_GPU) + '$'),
                CallbackQueryHandler(graph_for_gpu_func, pattern='^' + str(SHOW_60_DAYS_GPU) + '$'),
                CallbackQueryHandler(graph_for_gpu_func, pattern='^' + str(SHOW_90_DAYS_GPU) + '$'),
            ],
            ON_GPU_QUESTION: [
            ],
            GPU_SUBMENU: [
                MessageHandler(Filters.text, gpu_search_func),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(end_on_gpu, pattern='^' + str(BACK_TO_MENU) + '$'),
            CommandHandler('start', start_fallback),
        ],
        map_to_parent={
            BACK_TO_MENU: MENU
        },
    )

    # Добавление conversation handler с состояниями разговора
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                CallbackQueryHandler(stats_popularity_func, pattern='^' + str(STATS) + '$'),
                CallbackQueryHandler(stats_popularity_func, pattern='^' + str(POPULARITY) + '$'),
            ],
            STATS_SUBMENU: [
                CallbackQueryHandler(for_shop_vendor_stats, pattern='^' + str(FOR_SHOP) + '$'),
                CallbackQueryHandler(for_shop_vendor_stats, pattern='^' + str(FOR_VENDOR) + '$'),
                for_gpu_handler,
            ],
            POPULARITY_SUBMENU: [
                CallbackQueryHandler(for_shop_vendor_popularity, pattern='^'+ str(POPULARITY_FOR_SHOP) + '$'),
                CallbackQueryHandler(for_shop_vendor_popularity, pattern='^' + str(POPULARITY_FOR_VENDOR) + '$'),
            ],
            POPULARITY_SHOPS_SUBMENU: [
                CallbackQueryHandler(popularity_shops_graph, pattern='^' + str(DNS_SHOP) + '$'),
                CallbackQueryHandler(popularity_shops_graph, pattern='^' + str(MVIDEO_SHOP) + '$'),
                CallbackQueryHandler(popularity_shops_graph, pattern='^' + str(CITILINK_SHOP) + '$'),
            ],
            POPULARITY_SHOPS_GRAPH_SUBMENU: [
                CallbackQueryHandler(start_over, pattern='^' + str(BACK_TO_MENU) + '$')
            ],
            POPULARITY_VENDORS_SUBMENU: [
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_AFOX) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_ASROCK) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_ASUS) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_BIOSTAR) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_COLORFUL) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_DELL) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_EVGA) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_GIGABYTE) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_INNO3D) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_KFA2) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_MATROX) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_MSI) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_NVIDIA) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_PALIT) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_PNY) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_POWERCOLOR) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_SAPPHIRE) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_SINOTEX) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_XFX) + '$'),
                CallbackQueryHandler(popularity_vendors_graph, pattern='^' + str(VENDOR_ZOTAC) + '$'),
            ],
            POPULARITY_VENDORS_GRAPH_SUBMENU: [
                CallbackQueryHandler(start_over, pattern='^' + str(BACK_TO_MENU) + '$')
            ],
            SHOPS_SUBMENU: [
                CallbackQueryHandler(arch_func, pattern='^' + str(DNS_SHOP) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(MVIDEO_SHOP) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(CITILINK_SHOP) + '$'),
            ],
            VENDORS_SUBMENU: [
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_AFOX) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_ASROCK) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_ASUS) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_BIOSTAR) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_COLORFUL) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_DELL) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_EVGA) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_GIGABYTE) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_INNO3D) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_KFA2) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_MATROX) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_MSI) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_NVIDIA) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_PALIT) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_PNY) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_POWERCOLOR) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_SAPPHIRE) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_SINOTEX) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_XFX) + '$'),
                CallbackQueryHandler(arch_func, pattern='^' + str(VENDOR_ZOTAC) + '$'),
            ],
            ARCHITECTURE_SUBMENU: [
                CallbackQueryHandler(nvidia_amd_other_func, pattern='^' + str(NVIDIA) + '$'),
                CallbackQueryHandler(nvidia_amd_other_func, pattern='^' + str(AMD) + '$'),
                CallbackQueryHandler(nvidia_amd_other_func, pattern='^' + str(OTHER_ARCH) + '$'),
            ],
            OTHER_ARCH_SUBMENU: [
                CallbackQueryHandler(nvidia_amd_other_func, pattern='^' + str(INTEL) + '$'),
                CallbackQueryHandler(nvidia_amd_other_func, pattern='^' + str(MATROX) + '$'),
            ],
            NVIDIA_SERIES_SUBMENU: [
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_10XX_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_16XX_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_20XX_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_30XX_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_40XX_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_OTHER_SERIES) + '$'),
            ],
            NVIDIA_OTHER_SUBMENU: [
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_QUADRO_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_TESLA_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_GT_710_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_GT_730_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_210_SERIES) + '$'),
            ],
            NVIDIA_QUADRO_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_QUADRO_P2000_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_QUADRO_T400_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_QUADRO_RTX_6000_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_QUADRO_RTX_AXXXX_SERIES) + '$'),
            ],
            NVIDIA_QUADRO_RTX_AXXXX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_QUADRO_RTX_A2000_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_QUADRO_RTX_A4500_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_QUADRO_RTX_A5000_SERIES) + '$'),
            ],
            NVIDIA_TESLA_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_TESLA_A10_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_TESLA_A2_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_TESLA_T4_SERIES) + '$'),
            ],
            NVIDIA_10XX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_1080_TI_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_1050_TI_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_1030_SERIES) + '$'),
            ],
            NVIDIA_16XX_SERIES_SUBMENU: [
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_1660X_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_1650X_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_1630_SERIES) + '$'),
            ],
            NVIDIA_1650X_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_1650_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_1650_SUPER_SERIES) + '$'),
            ],
            NVIDIA_1660X_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_1660_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_1660_TI_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_1660_SUPER_SERIES) + '$'),
            ],
            NVIDIA_20XX_SERIES_SUBMENU: [
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_2060X_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_2080X_SERIES) + '$'),
            ],
            NVIDIA_2060X_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_2060_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_2060_SUPER_SERIES) + '$'),
            ],
            NVIDIA_2080X_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_2080_TI_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_2080_SUPER_SERIES) + '$'),
            ],
            NVIDIA_30XX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_3050_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_3060X_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_3070X_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_3080X_SERIES) + '$'),
                CallbackQueryHandler(nvidia_series_func, pattern='^' + str(NVIDIA_3090X_SERIES) + '$'),
            ],
            NVIDIA_3060X_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_3060_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_3060_TI_SERIES) + '$'),
            ],
            NVIDIA_3070X_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_3070_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_3070_TI_SERIES) + '$'),
            ],
            NVIDIA_3080X_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_3080_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_3080_TI_SERIES) + '$'),
            ],
            NVIDIA_3090X_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_3090_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_3090_TI_SERIES) + '$'),
            ],
            NVIDIA_40XX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_4080_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(NVIDIA_4090_SERIES) + '$'),
            ],
            AMD_SERIES_SUBMENU: [
                CallbackQueryHandler(amd_series_func, pattern='^' + str(AMD_RX5XX_SERIES) + '$'),
                CallbackQueryHandler(amd_series_func, pattern='^' + str(AMD_RX5XXX_SERIES) + '$'),
                CallbackQueryHandler(amd_series_func, pattern='^' + str(AMD_RX6XXX_SERIES) + '$'),
                CallbackQueryHandler(amd_series_func, pattern='^' + str(AMD_OTHER_SERIES) + '$'),
            ],
            AMD_OTHER_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_R7_240_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_R9_370_SERIES) + '$'),
            ],
            AMD_RX_5XX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_550_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_560_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_580_SERIES) + '$'),
            ],
            AMD_RX_5XXX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_5700_XT_SERIES) + '$')
            ],
            AMD_RX_6XXX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6400_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6500_XT_SERIES) + '$'),
                CallbackQueryHandler(amd_series_func, pattern='^' + str(AMD_RX_66XX_SERIES) + '$'),
                CallbackQueryHandler(amd_series_func, pattern='^' + str(AMD_RX_67XX_SERIES) + '$'),
                CallbackQueryHandler(amd_series_func, pattern='^' + str(AMD_RX_68XX_SERIES) + '$'),
                CallbackQueryHandler(amd_series_func, pattern='^' + str(AMD_RX_69XX_SERIES) + '$'),
            ],
            AMD_RX_66XX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6600_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6600_XT_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6650_XT_SERIES) + '$'),
            ],
            AMD_RX_67XX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6700_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6700_XT_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6750_XT_SERIES) + '$'),
            ],
            AMD_RX_68XX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6800_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6800_XT_SERIES) + '$'),
            ],
            AMD_RX_69XX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6900_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6900_XT_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(AMD_RX_6950_XT_SERIES) + '$'),
            ],
            INTEL_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(ARC_A310_SERIES) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(ARC_A380_SERIES) + '$'),
            ],
            MATROX_SERIES_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(MATROX_M9120_SERIES) + '$'),
            ],
            GRAPH_SUBMENU: [
                CallbackQueryHandler(graph_func, pattern='^' + str(GRAPH_MIN) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(GRAPH_AVERAGE) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(GRAPH_MAX) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(SHOW_30_DAYS) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(SHOW_60_DAYS) + '$'),
                CallbackQueryHandler(graph_func, pattern='^' + str(SHOW_90_DAYS) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(BACK_TO_MENU) + '$')
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
            MessageHandler(Filters.text & ~Filters.command, error_attention),
        ],
    )

    dispatcher.add_handler(conv_handler)

    # Регистрация команд - ответы в Telegram
    dispatcher.add_handler(CommandHandler('help', help_func))

    # Старт бота
    updater.start_polling()

    # Бот работает до прерывания Ctrl-C или получения stop команды
    updater.idle()


if __name__ == '__main__':
    main()
