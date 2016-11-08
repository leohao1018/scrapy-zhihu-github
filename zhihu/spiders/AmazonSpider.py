#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author Leo Hao
# OS Windows 7

from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest, Request


class AmazonSpider(CrawlSpider):
    name = 'AmazonSpider'
    allowed_domains = ['amazon.cn']
    # start_urls = ['http://associates.amazon.cn/gp/associates/network/main.html']

    start_urls = [
        'https://www.amazon.cn/ap/signin?_encoding=UTF8&openid.assoc_handle=cnflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.cn%2F%3Fref_%3Dnav_ya_signin']

    def __init__(self, *a, **kwargs):
        super(AmazonSpider, self).__init__(*a, **kwargs)
        self.http_user = 'liang.hao.1018@outlook.com'
        self.http_pass = '1qaz@WSX'
        # login form
        self.formdata = {'create': '0',
                         'email': self.http_user,
                         'password': self.http_pass,
                         }
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "www.amazon.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        }
        self.id = 0

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url,
                              meta={'cookiejar': i},
                              headers=self.headers,
                              callback=self.login)  # jump to login page

    def _log_page(self, response, filename):
        with open(filename, 'w') as f:
            f.write("%s\n%s\n%s\n" % (response.url, response.headers, response.body))

    def login(self, response):
        self._log_page(response, 'amazon_login.html')
        return [FormRequest.from_response(response,
                                          formdata=self.formdata,
                                          headers=self.headers,
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          callback=self.parse_item)]  # success login

    def parse_item(self, response):
        self._log_page(response, 'after_login.html')
        hxs = HtmlXPathSelector(response)
        report_urls = hxs.select('//div[@id="menuh"]/ul/li[4]/div//a/@href').extract()
        for report_url in report_urls:
            # print "list:"+report_url
            yield Request(self._ab_path(response, report_url),
                          headers=self.headers,
                          meta={'cookiejar': response.meta['cookiejar'],
                                },
                          callback=self.parse_report)

    def parse_report(self, response):
        self.id += 1
        self._log_page(response, "%d.html" % self.id)
