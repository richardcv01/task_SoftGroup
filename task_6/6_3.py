import aiohttp
import asyncio
from lxml import etree
import re
import itertools
import SQL_BD
import Mongo_DB

list_res = {}

async


def fetch(session, url):
    async
    with session.get(url, timeout=10) as response:
        return await
        response.text()


async


def get_url_title(session, list_url):
    list_title = []  # список назв усіх сторінок усіх тем
    list_url_title = []  # список urls усіх сторінок усіх тем
    list_author = []  # список авторів усіх сторінок усіх тем
    for url in list_url:
        response = await
        fetch(session, url)
        tree = etree.HTML(response)
        topic_a_node = tree.xpath("//a[@class='topictitle']")
        buff_title = []
        buff_href = []
        for element in topic_a_node:
            buff_title.append(element.text)
            buff_href.append(element.attrib['href'].split('&sid')[0])
        list_title.append(buff_title)
        list_url_title.append(buff_href)
        author = tree.xpath("//dd/a[@class='username' or @class='username-coloured']/text()")
        list_author.append(author)

    list_title_return = list(itertools.chain.from_iterable(list_title))
    list_url_title_return = list(itertools.chain.from_iterable(list_url_title))
    list_url_title_return_res = ['http://forum.overclockers.ua' + res[1:] for res in
                                 list_url_title_return]  # список url з насвою сайта (пвона адреса)
    list_author_return = list(itertools.chain.from_iterable(list_author))
    return {'list_title': list_title_return, 'list_url_title': list_url_title_return_res,
            'list_author': list_author_return}


async


def get_text_title(session, title, url, author):
    response = await
    session.get(url)
    text = await
    response.text()
    tree = etree.HTML(text)
    list_text_node = tree.xpath("//div[@class='content']")[0]
    list_text = list_text_node.xpath('./descendant-or-self::text()')
    text = await
    clear_text(list_text)
    price, currency = await
    price_currency(text)
    if price != 0:
        price = int(price)
    return await
    write_database(title, url, author, text, price, currency, 'mongo')


async


def clear_text(list_text):
    text = ' '.join(list_text)
    text = re.sub(r'[\s]', ' ', text)
    text = re.sub(r'(\b)+(http)s?://.*?\s|(\b)+(http)s?://.*\b|(\b)+ftp?://.*?\s|(спойлер)+', ' ', text)
    # text = re.sub(r"(спойлер)+ ", ' ', text)
    text = re.sub(r'[-,=,_,*]+|[\s]', ' ', text)
    return text


async


def write_database(title, url, author, text, price, currency, type_db='postgree'):
    dicfun = {'postgree': SQL_BD.insertBD, 'mongo': mongo_base.insert}
    dicfun[type_db](title, url, author, text, price, currency)


async


def write_file_json(title, url, author, text, price, currency):
    dic = {'title': title, 'url': url, 'author': author, 'text': text, 'price': price, 'currency': currency}
    with open('text.txt', 'a', encoding='utf-8') as file:
        file.write(str(dic) + '\n')


async


def price_currency(text):
    dic = {'грн': re.compile(r"(\d+)[\s]*грн"), '$': re.compile(r"(\d+)[\s]*[\$, долларов]")}
    list_p_c = []
    for key, val in dic.items():
        lis = [int(i) for i in val.findall(text)]
        lis = list(filter(None, lis))
        if lis:
            price = min(lis)
        else:
            price = None
        list_p_c.append((price, key))
    list_price_currency = [[price, curren] for price, curren in (list_p_c[0], list_p_c[1]) if price != None]
    if list_price_currency:
        price_res = list_price_currency[0][0]
        currency_res = list_price_currency[0][1]
    else:
        price_res = 0
        currency_res = 'грн'
    return price_res, currency_res


async


def main(loop):
    async
    with aiohttp.ClientSession(loop=loop) as session:
        list_url_text_title = get_url_title(session, get_url_page(3))
        list_url = await
        list_url_text_title
        tasks = [(get_text_title(session, title, url, author)) for title, url, author in
                 zip(list_url['list_title'], list_url['list_url_title'], list_url['list_author'])]
        await
        asyncio.gather(*tasks)


def get_url_page(count=1):
    """
    :param count: кількість сторінок
    :return: Список urls сторінок з темами
    """
    list_url_page = []
    list_url_page.append('http://forum.overclockers.ua/viewforum.php?f=26')
    for i in range(count - 1):
        list_url_page.append('http://forum.overclockers.ua/viewforum.php?f=26&start=' + str((i + 1) * 40))
    return list_url_page


event_loop = asyncio.get_event_loop()
mongo_base = Mongo_DB.Mongo()
try:
    event_loop.run_until_complete(main(event_loop))
    SQL_BD.close()
finally:
    event_loop.close()


