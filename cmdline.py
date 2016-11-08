#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author Leo Hao
# OS Windows 7

import scrapy.cmdline

if __name__ == '__main__':
    scrapy.cmdline.execute(["scrapy", "crawl", "AmazonSpider"])
