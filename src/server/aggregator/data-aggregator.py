import datetime
import json
import math
import os
import re
import time
import schedule

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def get_data_mvideo(date):
    print('[INFO] Started Mvideo data aggregation')

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
                           cookies=cookies, headers=headers)

    print(f'[RESPONSE] /products/listing - {response}')
    total_items = response.json().get('body').get('total')

    if total_items is None:
        return '[!] No items!'

    page_limit = int(params.get('limit'))

    pages_count = math.ceil(total_items / page_limit)

    print(f'[INFO] Total positions: {total_items} | Total pages: {pages_count}')

    products_ids = {}
    products_descriptions = {}
    products_prices = {}

    for i in range(pages_count):
        time.sleep(3)
        offset = f'{i * page_limit}'

        params = {
            'categoryId': '5429',
            'offset': offset,
            'limit': '24',
            'doTranslit': 'true',
        }

        response = session.get('https://www.mvideo.ru/bff/products/listing', params=params,
                               cookies=cookies, headers=headers)
        print(f'[RESPONSE] /products/listing - {response}')
        products_ids_list = response.json().get('body').get('products')
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

        time.sleep(1)
        response = session.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies,
                                headers=headers, json=json_data)
        print(f'[RESPONSE] /product-details/list - {response}')
        products_descriptions[i] = response.json()

        products_ids_str = ','.join(products_ids_list)

        params = {
            'productIds': products_ids_str,
            'addBonusRubles': 'true',
            'isPromoApplied': 'true',
        }

        time.sleep(1)
        response = session.get('https://www.mvideo.ru/bff/products/prices', params=params,
                               cookies=cookies, headers=headers)
        print(f'[RESPONSE] /products/prices - {response}')
        material_prices = response.json().get('body').get('materialPrices')

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

            name = item.get('modelName').upper()
            name = insert_spaces(name)
            name = remove_extra_repeats(name)

            if 'PCIE16' in name:
                name = name.replace('PCIE16', '')
            if 'LHR' in name:
                name = name.replace('LHR', '')
            if 'PCIE' in name:
                name = name.replace('PCIE', '')
            if 'PCI-EXPS' in name:
                name = name.replace('PCI-EXPS', '')
            if 'LOW PROFILE' in name:
                name = name.replace('LOW PROFILE', '')
            if re.search('RX', name):
                name = name.replace('RX', 'RX ', 1)
            if re.search('GT[0-9]+', name):
                name = name.replace('GT', 'GT ', 1)
            if re.search('GTX[0-9]+', name):
                name = name.replace('GTX', 'GTX ', 1)
            if re.search('RTX[0-9]+', name):
                name = name.replace('RTX', 'RTX ', 1)
            if re.search('[0-9]XT', name):
                name = name.replace('XT', ' XT', 1)
            if re.search('[0-9]XTX', name):
                name = name.replace('XTX', ' XTX', 1)

            name_title = name.split()

            vendor = item.get('brandName').upper()
            model_name = item.get('propertiesPortion')[-1].get('value').upper()
            architecture_label = model_name.upper().split(' ')[0]
            if architecture_label == 'GEFORCE':
                architecture = 'NVIDIA'
                if name_title[0] != 'GEFORCE':
                    name_title.insert(0, 'GEFORCE')
            elif architecture_label == 'RADEON':
                architecture = 'AMD'
                if name_title[0] != 'RADEON':
                    name_title.insert(0, 'RADEON')
            else:
                print(f'[INFO] Found unknown architecture - {architecture_label}')
                architecture = 'UNKNOWN'

            name = ' '.join(name_title)
            name = remove_repeats(name)

            if '(' in name:
                name = name[:name.index('(')]

            name = remove_repeated_gb_tags(name)

            series = model_name

            if name.startswith('GEFORCE RTX 3060 TI'):
                series = 'GEFORCE RTX 3060 TI'

            if re.search('[0-9]XT', series):
                series = series.replace('XT', ' XT')
            if re.search('[0-9]XTX', series):
                series = series.replace('XTX', ' XTX')

            offers_list.append(Offer(name, architecture, series, 'MVIDEO',
                                     vendor, price, popularity, date))
            popularity += 1

    session.close()

    return offers_list


def get_data_citilink(date):
    print('[INFO] Started CitiLink data aggregation')

    url = 'https://www.citilink.ru/catalog/videokarty/?sorting=popularity_asc'
    response = requests.get(url=url)
    print(f'[RESPONSE] /catalog/videokarty - {response}')
    soup = BeautifulSoup(response.text, 'html.parser')

    total_items = int(soup.find('div', class_='Subcategory__count').text.split()[0])

    page_limit = 0
    for _ in soup.findAll('div', class_='product_data__gtm-js'):
        page_limit += 1

    pages_count = math.ceil(total_items / page_limit)

    print(f'[INFO] Total positions: {total_items} | Total pages: {pages_count}')

    offers_list = []
    popularity = 0
    for page in range(1, pages_count + 1):
        current_page_url = f'{url}&p={page}'
        time.sleep(3)
        response = requests.get(url=current_page_url)
        print(f'[RESPONSE] /catalog/videokarty/?p={page} - {response}')
        soup = BeautifulSoup(response.text, 'html.parser')

        for product in soup.findAll('div', class_='product_data__gtm-js'):
            name_title = product.find('a', class_='ProductCardHorizontal__title')['title'].split()
            for i in range(len(name_title)):
                name_title[i] = name_title[i].upper()

            if name_title[3] != 'GEFORCE':
                if name_title[2] == 'NVIDIA':
                    name_title.insert(3, 'GEFORCE')
                elif name_title[2] == 'AMD':
                    name_title.insert(3, 'RADEON')

            name = ''
            if 'RET' in name_title:
                name = ' '.join(name_title[3:name_title.index('RET')])
            elif 'RET(ВОССТАНОВЛЕННЫЙ)' in name_title:
                name = ' '.join(name_title[3:name_title.index('RET(ВОССТАНОВЛЕННЫЙ)')])
            elif 'BULK' in name_title:
                name = ' '.join(name_title[3:name_title.index('BULK')])
            elif 'OEM' in name_title:
                name = ' '.join(name_title[3:name_title.index('OEM')])
            else:
                name = ' '.join(name_title[3:])

            if ',' in name:
                name = name.replace(',', '')
            if 'LHR' in name:
                name = name.replace('LHR', '')
            if 'LOW PROFILE' in name:
                name = name.replace('LOW PROFILE', '')
            if 'BULK' in name:
                name = name.replace('BULK', '')
            if ' RU' in name:
                name = name.replace(' RU', '')

            name = insert_spaces(name)
            name = remove_repeats(name)
            name = remove_extra_repeats(name)

            vendor = name_title[1]
            properties_title = product.findAll('li', class_='ProductCardHorizontal__properties_item')

            architecture, series = '', ''
            for property_title in properties_title:
                if 'Видеочипсет' in property_title.text.split()[0]:
                    series_title = property_title.text.split(',', 1)[0].split()
                    series = ' '.join(series_title[2:5]).upper()
                    if series[-2:] == 'TI':
                        series = series.replace('TI', ' TI')
                    elif series[-5:] == 'SUPER':
                        series = series.replace('SUPER', ' SUPER')
                    elif series[-2:] == 'XT':
                        series = series.replace('XT', ' XT')
                    elif series[-2:] == 'XTX':
                        series = series.replace('XTX', ' XTX')

                    architecture = series_title[1]

            price_title = product.find('span', class_='ProductCardHorizontal__price_current-price')
            price = 0
            if price_title is not None:
                popularity += 1
                price_title = price_title.text.split()
                price_number_str = ''
                for num in price_title:
                    price_number_str += num
                price = int(price_number_str)
                offers_list.append(Offer(name, architecture, series, 'CITILINK',
                                         vendor, price, popularity, date))

        print(f'[+] Finished {page} of the {pages_count} pages')

    print(f'[INFO] Positions with price: {popularity} | Total positions: {total_items}')

    return offers_list


def get_data_dns(date):
    print('[INFO] Started DNS data aggregation')

    offers_list = []

    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')

    options.add_argument("--headless")

    options.add_argument('--disable-blink-features=AutomationControlled')

    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(chrome_options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    url = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?order=6'

    try:
        driver.get(url=url)
        print(f'[RESPONSE] /videokarty/?order=6 - <Response [200]>')
        time.sleep(10)
        page_title = driver.find_element(By.XPATH,
                                         './/span[@class="products-count"]').text.split(' ')
        total_items = int(page_title[0])

        pagination_ref = driver.find_element(By.CSS_SELECTOR,
                                             f'#products-list-pagination > ul > '
                                             f'li:nth-child(12) > a').get_attribute('href')
        page_attribute_index = pagination_ref.index('=')
        pages_count = int(pagination_ref[page_attribute_index + 1:])

        page_limit = math.ceil(total_items / pages_count)

        if page_limit != 18:
            print(f'[INFO] Non-standard page limit: {page_limit}')

        print(f'[INFO] Total positions: {total_items} | Total pages: {pages_count}')

        for page in range(1, pages_count):
            current_page_url = f'{url}&p={page}'
            time.sleep(10)
            driver.get(url=current_page_url)
            print(f'[RESPONSE] /catalog/videokarty/?p={page} - <Response [200]>')

            collect_items_dns(driver, page_limit, page_limit, page, date, offers_list)

            print(f'[+] Finished {page} of the {pages_count} pages')

        last_page_url = f'{url}&p={pages_count}'
        time.sleep(10)
        driver.get(url=last_page_url)
        print(f'[RESPONSE] /catalog/videokarty/?p={pages_count} - <Response [200]>')

        last_page_limit = total_items - (pages_count - 1) * page_limit

        collect_items_dns(driver, last_page_limit, page_limit, pages_count, date, offers_list)

        print(f'[+] Finished {pages_count} of the {pages_count} pages')

        time.sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    return offers_list


def collect_items_dns(driver, page_limit, popularity_limit, page, date, offers_list):
    first_elem = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          f'body > div.container.category-child > div > '
                                          f'div.products-page__content > div.products-page__list > '
                                          f'div.products-list > div > div.catalog-products.view-simple > '
                                          f'div:nth-child(1) > '
                                          f'div.product-buy.product-buy_one-line.catalog-product__buy > '
                                          f'div'))
    ).text.split('\n')

    block = driver.find_element(By.CLASS_NAME, 'products-list__content')
    for item_id in range(1, page_limit + 1):
        tries_counter = 0
        for attempt in range(10):
            try:
                item_price = driver.find_element(By.CSS_SELECTOR,
                                                 f'body > div.container.category-child > '
                                                 f'div > div.products-page__content > '
                                                 f'div.products-page__list > div.products-list > '
                                                 f'div > div.catalog-products.view-simple > '
                                                 f'div:nth-child({item_id}) > '
                                                 f'div.product-buy.product-buy_one-line.catalog-product__buy > '
                                                 f'div > div.product-buy__price')
            except NoSuchElementException:
                tries_counter += 1
            else:
                break

        if tries_counter == 10:
            print(f'[INFO] Item {item_id} on page {page} has no price for 10 attempts')
        else:
            item = block.find_element(By.CSS_SELECTOR,
                                      f'body > div.container.category-child > div > '
                                      f'div.products-page__content > div > div.products-list > '
                                      f'div > div.catalog-products.view-simple > '
                                      f'div:nth-child({item_id})').text.split('\n')
            popularity = (page - 1) * popularity_limit + item_id

            card_name, card_architecture, card_series, card_shop, card_vendor, card_price, \
                card_popularity, card_date = get_attributes_dns(item, popularity, date)
            if card_price > 0:
                offers_list.append(Offer(
                    card_name,
                    card_architecture,
                    card_series,
                    card_shop,
                    card_vendor,
                    card_price,
                    card_popularity,
                    card_date
                ))


def insert_spaces(title):
    if 'TI ' in title:
        title = title.replace('TI ', ' TI ')
    elif 'SUPER' in title:
        title = title.replace('SUPER ', ' SUPER ')
    elif 'XT ' in title:
        title = title.replace('XT ', ' XT ')
    elif 'XTX ' in title:
        title = title.replace('XTX ', ' XTX ')

    title = title.replace('  ', ' ')

    return title


def remove_repeats(title):
    title = title.split()

    for word in title:
        first_index = title.index(word)
        counter = title.count(word)

        if counter > 1:
            for _ in range(counter):
                title.remove(word)

            title.insert(first_index, word)

    title = ' '.join(title)
    return title


def remove_extra_repeats(title):
    title = title.split()

    for word in title:
        if word.endswith('ГБ'):
            title.remove(word)

    for word in title:
        if word.__contains__('DDR'):
            title.remove(word)

    title = ' '.join(title)

    return title


def remove_repeated_gb_tags(title):
    title = title.split()

    g_counter, gb_counter, gd_counter = 0, 0, 0
    for word in title:
        if word.__contains__('GB'):
            gb_counter += 1
        if re.search('[0-9]+G$', word):
            g_counter += 1
        if re.search('[0-9]+GD$', word):
            gd_counter += 1

    if gb_counter >= 1 and g_counter >= 1:
        for word in title:
            if re.search('[0-9]+G$', word):
                title.remove(word)
    elif gb_counter >= 1 and gd_counter >= 1 or g_counter >= 1 and gd_counter >= 1:
        for word in title:
            if re.search('[0-9]+GD$', word):
                title.remove(word)

    title = ' '.join(title)

    return title


def get_attributes_dns(title, popularity, date):
    name = ''
    if re.search('-[0-9]+%$', title[0]):
        name = title[1].upper()
    else:
        name = title[0].upper()

    name = name[0:name.index('[')].split()[1:]
    vendor = name[0]
    architecture, series = '', ''
    for tag in name:
        if 'GEFORCE' in tag or 'QUADRO' in tag:
            architecture = 'NVIDIA'
            arch_index = name.index(tag)
            series_title = name[arch_index:]

            if len(series_title) >= 4:
                if 'TI' in series_title:
                    extra_index = series_title.index('TI')
                    series = ' '.join(series_title[:extra_index + 1])
                elif 'SUPER' in series_title:
                    extra_index = series_title.index('SUPER')
                    series = ' '.join(series_title[:extra_index + 1])
                else:
                    series = f'{series_title[0]} {series_title[1]} {series_title[2]}'
            elif len(series_title) == 3:
                series = f'{series_title[0]} {series_title[1]} {series_title[2]}'
            elif len(series_title) == 2:
                series = f'{series_title[0]} {series_title[1]}'
            break
        elif 'TESLA' in tag:
            architecture = 'NVIDIA'
            if name[2] == 'NVIDIA':
                series = f'{name[1]} {name[3]} {name[4]}'
            elif len(name) > 3:
                series = f'{name[1]} {name[2]} {name[3]}'
            elif len(name) == 3:
                series = f'{name[1]} {name[2]}'
            break
        elif 'RADEON' in tag:
            architecture = 'AMD'
            arch_index = name.index(tag)
            series_title = name[arch_index:]

            if len(series_title) >= 4:
                if 'XT' in series_title:
                    extra_index = series_title.index('XT')
                    series = ' '.join(series_title[:extra_index + 1])
                elif 'XTX' in series_title:
                    extra_index = series_title.index('XTX')
                    series = ' '.join(series_title[:extra_index + 1])
                else:
                    series = f'{series_title[0]} {series_title[1]} {series_title[2]}'
            elif len(series_title) >= 3:
                series = f'{series_title[0]} {series_title[1]} {series_title[2]}'
            break
        elif 'INTEL' in tag:
            architecture = 'INTEL'
            series = f'{name[1]} {name[2]} {name[3]}'
            break
        elif 'MATROX' in tag:
            architecture = 'MATROX'
            series = f'{name[1]}'
            break
        elif 'GTX' in tag:
            architecture = 'NVIDIA'
            series = f'{name[1]} {name[2]}'
            break
        elif 'NVIDIA' in tag:
            architecture = 'NVIDIA'
            if len(name) >= 4:
                if name[2] == 'RTX':
                    series = f'QUADRO {name[2]} {name[3]}'
                    break
                else:
                    series = 'UNKNOWN'
            else:
                series = 'UNKNOWN'
        elif re.search('RX[0-9]+$', tag):
            architecture = 'AMD'
            series = f'RADEON {tag}'
            series = series.replace('RX', 'RX ')
            break
        else:
            architecture, series = 'UNKNOWN', 'UNKNOWN'

    name = ' '.join(name)

    name = insert_spaces(name)

    if re.search('RX[0-9]+', name):
        name = name.replace('RX', 'RX ')

    if re.search('RX[0-9]+', series):
        series = series.replace('RX', 'RX ')

    for extra_tag in ['XT', 'XTX', 'TI', 'SUPER']:
        if re.search(f'[0-9]+{extra_tag}$', series):
            series = series.replace(extra_tag, f' {extra_tag}')

    shop = 'DNS'
    item_prices = []
    for tag in title:
        if '₽' in tag and 'мес.' not in tag:
            item_prices.append(int(''.join(tag.split()[:-1])))

    if len(item_prices) != 0:
        price = min(item_prices)
    else:
        price = -1

    return name, architecture, series, shop, vendor, price, popularity, date


def main():
    date = str(datetime.date.today())
    print(f'[INFO] Started data aggregation - {date}')

    shops_list = {
        "MVIDEO": get_data_mvideo(date),
        "CITILINK": get_data_citilink(date),
        "DNS": get_data_dns(date)
    }

    json_string = json.dumps(shops_list, indent=4, ensure_ascii=False, default=lambda x: x.__dict__)
    with open(f'data/offers-{date}.json', 'w', encoding='utf-8') as file:
        file.write(json_string)

    # Отправка данных на сервер
    response = requests.post(url='http://localhost:8080/insert-new-data', json=data)
    print(f'[INFO] Response: {response}')


if __name__ == '__main__':
    schedule.every().day.at("01:00").do(main)
    schedule.every().day.at("05:15").do(main)
    while 1:
        schedule.run_pending()
        time.sleep(1)
