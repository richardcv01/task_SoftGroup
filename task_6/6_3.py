import aiohttp
import asyncio
import async_timeout
from lxml import etree
import re
import itertools

list_res = {}

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def get_url_title(list_url):
    list_title = []  # список назв усіх сторінок усіх тем
    list_url_title = [] #список urls усіх сторінок усіх тем
    list_author = []  # список авторів усіх сторінок усіх тем
    session1 = aiohttp.ClientSession()
    for url in list_url:
        response = await fetch(session1, url)
        tree = etree.HTML(response)
        title =tree.xpath("//a[@class='topictitle']/text()")
        href = tree.xpath("//a[@class='topictitle']/@href")
        #topic = tree.xpath("//a[@class='topictitle']")
        author= tree.xpath("//dd/a[@class='username']/text() | //dd/a[@class='username-coloured']/text()")
        list_title.append(title)
        list_url_title.append(href)
        list_author.append(author)
    session1.close()
    list_title_return = list(itertools.chain.from_iterable(list_title))
    list_url_title_return = list(itertools.chain.from_iterable(list_url_title))
    list_url_title_return_res = ['http://forum.overclockers.ua'+res[1:] for res in list_url_title_return] #список url з насвою сайта (пвона адреса)
    list_author_return = list(itertools.chain.from_iterable(list_author))
    return {'list_title':list_title_return, 'list_url_title':list_url_title_return_res, 'list_author':list_author_return}

async def get_text_title(session, title, url, author):
    response = await session.get(url)
    tit = title
    text = await response.text()
    response.close()
    tree = etree.HTML(text)
    list_text = tree.xpath("//div[@class='notice']/preceding::div[@class='content']/descendant-or-self::text()")
    text = ' '.join(list_text)
    price, currency = price_currency(text)
    return await write_file_json(title, url, author,text, price, currency)
    #return text

async def write_file_json(title, url, author, text, price, currency):
    dic = {'title': title, 'url': url, 'author': author, 'text': text, 'price':price, 'currency':currency}
    with open('text.txt', 'a', encoding='utf-8') as file:
        file.write(str(dic) + '\n')

def price_currency(text):
    dic = {'грн': re.compile(r"(\d+)[\s]*грн"), '$': re.compile(r"(\d)+[\s]*\$")}
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
        price_res = None
        currency_res = None
    return price_res, currency_res

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        list_url_text_title = get_url_title(get_url_page(2))
        list_url = await list_url_text_title
        tasks = [asyncio.Task(get_text_title(session, title, url, author)) for title, url, author in
                 zip(list_url['list_title'], list_url['list_url_title'], list_url['list_author'])]
        await asyncio.gather(*tasks)
        #for title, url, author in zip(list_url['list_title'], list_url['list_url_title'], list_url['list_author']):
            #await get_text_title(session, title, url, author)

def get_url_page(count=1):
    """
    :param count: кількість сторінок
    :return: Список urls сторінок з темами
    """
    list_url_page = []
    list_url_page.append('http://forum.overclockers.ua/viewforum.php?f=26')
    for i in range(count-1):
        list_url_page.append('http://forum.overclockers.ua/viewforum.php?f=26&start=' + str((i+1)*40))
    return list_url_page


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()


