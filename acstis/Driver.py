# -*- coding: utf-8 -*-

# MIT License
# 
# Copyright (c) 2017 Tijme Gommers
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from nyawc.Options import Options
from nyawc.Queue import QueueItem
from nyawc.Crawler import Crawler, CrawlerActions
from nyawc.http.Request import Request
from acstis.Logging import Logging
from acstis.Exploit import Exploit
from acstis.Scraper import Scraper

import requests
import sys

class Driver:

    input_uri = None

    input_help = False

    input_verify_exploit = False

    input_use_crawler = False

    input_quit_if_vulnerable = False

    crawler_options = Options()
    
    website_details = None

    vulnerable_requests = []

    def __init__(self, uri, verify_exploit, use_crawler, quit_if_vulnerable):
        Logging.info("Started scan");

        self.input_uri = uri
        self.input_verify_exploit = verify_exploit
        self.input_use_crawler = use_crawler
        self.input_quit_if_vulnerable = quit_if_vulnerable

        self.crawler_options.callbacks.crawler_before_start = self.cb_crawler_before_start
        self.crawler_options.callbacks.crawler_after_finish = self.cb_crawler_after_finish
        self.crawler_options.callbacks.request_before_start = self.cb_request_before_start
        self.crawler_options.callbacks.request_after_finish = self.cb_request_after_finish

        self.crawler_options.scope.protocol_must_match = False
        self.crawler_options.scope.subdomain_must_match = True
        self.crawler_options.scope.domain_must_match = True
        self.crawler_options.scope.ignore_similar_requests = True
        self.crawler_options.scope.max_depth = 0 if not self.input_use_crawler else None 

        self.crawler_options.performance.max_threads = 8

        try:
            self.website_details = Scraper.get_details(self.input_uri);
        except Exception as e:
            Logging.red("Error while scraping URL '{}': {}".format(self.input_uri, str(e)))
            return

        if not self.website_details["uses_angular"]:
            Logging.red("This website does not use AngularJS.")
            return

        Logging.info("Found AngularJS version " + self.website_details["angular_version"])

        crawler = Crawler(self.crawler_options)
        crawler.start_with(Request(self.input_uri))

    def cb_crawler_before_start(self):
        Logging.info("Started crawler");

    def cb_crawler_after_finish(self, queue):
        Logging.info("Found {} vulnerable URI(s)".format(len(self.vulnerable_requests)))

    def cb_request_before_start(self, queue, queue_item):
        result = Exploit.is_vulnerable(queue_item, self.website_details["angular_version"], self.input_verify_exploit)

        if result is not False:
            self.vulnerable_requests.append(result);
            Logging.red("Request is vulnerable [" + result.request.method + "] " + result.request.url + " (PostData: " + str(result.request.data) + ")")

            if self.input_quit_if_vulnerable:
                return CrawlerActions.DO_STOP_CRAWLING

        return CrawlerActions.DO_CONTINUE_CRAWLING

    def cb_request_after_finish(self, queue, queue_item, new_queue_items):
        return CrawlerActions.DO_CONTINUE_CRAWLING