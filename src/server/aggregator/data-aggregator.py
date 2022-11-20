import datetime
import json
import math
import os

import requests

from config import headers, cookies


class Offer:

    def __init__(self, card_name, card_architecture, card_series, shop_name,
                 vendor_name, card_price, card_popularity, date):
        self.cardName = card_name
        self.cardArchitecture = card_architecture
        self.cardSeries = card_series
        self.shopName = shop_name
        self.vendorName = vendor_name
        self.cardPrice = card_price
        self.cardPopularity = card_popularity
        self.date = date

    def __str__(self):
        return f'{self.shopName} {self.vendorName} {self.cardArchitecture}' \
               f' {self.cardName} {self.cardPrice} {self.cardPopularity} {self.date}'


def get_data_mvideo():

    date = str(datetime.date.today())

    params = {
        'categoryId': '5429',
        'offset': '0',
        'limit': '24',
        'doTranslit': 'true',
    }

    if not os.path.exists('data'):
        os.mkdir('data')

    session = requests.Session()
    response = session.get('https://www.mvideo.ru/bff/products/listing', params=params,
                           cookies=cookies, headers=headers).json()

    total_items = response.get('body').get('total')

    if total_items is None:
        return '[!] No items!'

    page_limit = int(params.get('limit'))

    pages_count = math.ceil(total_items / page_limit)

    print(f'[INFO] Total positions: {total_items} | Total pages: {pages_count}')

    products_ids = {}
    products_descriptions = {}
    products_prices = {}

    for i in range(pages_count):
        offset = f'{i * page_limit}'

        params = {
            'categoryId': '5429',
            'offset': offset,
            'limit': '24',
            'doTranslit': 'true',
        }

        response = session.get('https://www.mvideo.ru/bff/products/listing', params=params,
                               cookies=cookies, headers=headers).json()

        products_ids_list = response.get('body').get('products')
        products_ids[i] = products_ids_list

        json_data = {
            'productIds': products_ids_list,
            'mediaTypes': [
                'images',
            ],
            'category': True,
            'status': True,
            'brand': True,
            'propertyTypes': [
                'KEY',
            ],
            'propertiesConfig': {
                'propertiesPortionSize': 20,
            },
            'multioffer': False,
        }

        response = session.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies,
                                headers=headers, json=json_data).json()
        products_descriptions[i] = response

        products_ids_str = ','.join(products_ids_list)

        params = {
            'productIds': products_ids_str,
            'addBonusRubles': 'true',
            'isPromoApplied': 'true',
        }

        response = session.get('https://www.mvideo.ru/bff/products/prices', params=params,
                               cookies=cookies, headers=headers).json()
        material_prices = response.get('body').get('materialPrices')

        for item in material_prices:
            item_id = item.get('price').get('productId')
            item_base_price = item.get('price').get('basePrice')
            item_sale_price = item.get('price').get('salePrice')

            products_prices[item_id] = {
                'item_base_price': item_base_price,
                'item_sale_price': item_sale_price
            }

        print(f'[+] Finished {i + 1} of the {pages_count} pages')

    offers_list = []
    popularity = 1
    for items in products_descriptions.values():
        products = items.get('body').get('products')

        for item in products:
            product_id = item.get('productId')

            price = 0
            if product_id in products_prices:
                prices = products_prices[product_id]
                base_price = prices.get('item_base_price')
                sale_price = prices.get('item_sale_price')
                price = min(base_price, sale_price)

            name = item.get('modelName')
            vendor = item.get('brandName')
            model_name = item.get('propertiesPortion')[-1].get('value')
            architecture_label = model_name.upper().split(' ')[0]
            if architecture_label == 'GEFORCE':
                architecture = 'NVIDIA'
            elif architecture_label == 'RADEON':
                architecture = 'AMD'
            else:
                print(f'[INFO] Found unknown architecture - {architecture_label}')
                architecture = 'UNKNOWN'

            series = model_name
            offers_list.append(Offer(name, architecture, series, 'Mvideo',
                                     vendor, price, popularity, date))
            popularity += 1

    json_string = json.dumps([ob.__dict__ for ob in offers_list], indent=4, ensure_ascii=False)
    with open(f'data/mvideo-offers-{date}.json', 'w', encoding='utf-8') as file:
        file.write(json_string)


def main():
    get_data_mvideo()


if __name__ == '__main__':
    main()
