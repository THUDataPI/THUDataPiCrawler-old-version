# -*- coding: utf-8 -*-

from scrapy import cmdline

cmdline.execute("scrapy crawl THUDataPiCrawler_chinahr -s CLOSESPIDER_ITEMCOUNT=300".split())