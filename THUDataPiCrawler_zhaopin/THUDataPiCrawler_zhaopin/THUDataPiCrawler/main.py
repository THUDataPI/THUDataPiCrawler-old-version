# -*- coding: utf-8 -*-

from scrapy import cmdline

cmdline.execute("scrapy crawl THUDataPiCrawler_jobs_zhaopin -s CLOSESPIDER_ITEMCOUNT=5000".split())