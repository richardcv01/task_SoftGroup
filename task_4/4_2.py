#log.py
#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import requests
from lxml import html
import threading
import queue

logging.basicConfig(level=logging.INFO)


class Scraper:
    def __init__(self, query, page_from, page_to, limit=2):
        self.query = query
        self.page_from = page_from
        self.page_to = page_to + 1
        self.limit = limit

    def __prepare(self):
        HEADERS = {
                'Accept':
'text/html,application/xhtml+xml,application/xml;q=0.9,image/web'
'p,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, lzma, sdch',
            'Accept-Language': 'ru-RU,ru;q=0.8,enUS;q=0.6,en;q=0.4',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.olx.ua',
            'Referer': 'https://www.olx.ua/',
            'Save-Data': 'on',
            'Upgrade-Insecure-Requests': '1',
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99'
'Safari/537.36 OPR/41.0.2353.69',
        }

        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def start(self):
        self.lis = []
        self.__prepare()
        #url = self.get_link(3)
        #self.notify(url)
        #return self.crawl(url)
        self.multi()
        return self.lis

    def pr(self):
        while self.clientPool:
            url = self.clientPool.get()
            #
            res = self.crawl(url)
            self.notify(url)
            print(res)
        return res

            #print(url)



    def multi(self):
        self.clientPool = queue.Queue(0)

        for j in range(1,5+1):
            self.url = self.get_link(j)
            self.clientPool.put(self.url)
        for i in range(1, self.limit+1):
            t = threading.Thread(target=self.pr)
            t.start()




        #while self.ii:
            #url = self.get_link(self.ii)
            #self.clientPool.put(url)
            #self.ii=self.ii-1


    def get_link(self, page):
        link = 'https://www.olx.ua/chernovtsy/q-{0}/?page={1}'.format(self.query, page)
        return link

    def notify(self, url):
        logging.info('Task done:' + url)

    def crawl(self, url):
        resp = self.session.get(url)

        if resp.status_code == 200:
            page = resp.text
            root = html.fromstring(page)
            items = []
            offers = root.xpath('//td[@class="offer "]')
            for offer in offers:
                try:
                    title = offer.xpath('.//div[@class="space rel"]/h3/a/strong/text()')[0]
                    price = offer.xpath('.//td[@class="wwnormal tright td-price"]//p/strong/text()')[0]
                    items.append((title, price))
                except:
                    print('error')
                    pass

            return items

scrapper = Scraper('iphone', 1, 2, limit=2)
results = scrapper.start()
#scrapper.multi()
for result in results:
    offer, price = result
    #print(offer, price)