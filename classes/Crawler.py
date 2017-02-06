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

from urllib.parse import urlparse, urlencode, parse_qs, quote_plus
from urllib.request import urlopen
from bs4 import BeautifulSoup

import sys 

"""

"""
class Crawler:

    """
    Keep track of the Crawler instance
    """
    _instance = None

    """
    
    """
    def get_urls(self, uri):
        found_uris = []

        # ToDo: Make this recursive until all uri's have been crawled.

        contents = self.get_contents(uri)
        soup = BeautifulSoup(contents, "html.parser")

        uris_by_href = self.find_uris_by_href(uri, soup)
        found_uris= self.merge_uris_without_duplicates(found_uris, uris_by_href)

        uris_by_forms = self.find_uris_by_forms(uri, soup)
        found_uris= self.merge_uris_without_duplicates(found_uris, uris_by_forms)

        found_uris.append(uri)
        found_uris.append(uri + "?canonical=check")
        found_uris.append(uri + "&canonical=check")

        return found_uris

    """
    
    """
    def merge_uris_without_duplicates(self, existing_uris, new_uris):
        for new_uri in new_uris:
            already_in = False
            for existing_uri in existing_uris:
                if self.url_is_essentially_the_same(existing_uri, new_uri):
                    already_in = True
                    break

            if not already_in:
                existing_uris.append(new_uri)

        return existing_uris

    """
    Get all the query params in the given URL
    """
    def get_params(self, url):
        parsed = urlparse(url)
        return parse_qs(parsed.query)

    """
    
    """
    def url_is_essentially_the_same(self, existing_uri, new_uri):
        existing_uri_params = self.get_params(existing_uri)
        new_uri_params = self.get_params(new_uri)

        if self.get_base(existing_uri) == self.get_base(new_uri) and len(existing_uri_params) == len(new_uri_params):
            return True

        param_keys_do_not_match = False

        for existing_uri_param in existing_uri_params:
            param_exists_in_both = False
            for new_uri_param in new_uri_params:
                if new_uri_param == existing_uri_param:
                    param_exists_in_both = True
                    break

            if not param_exists_in_both:
                param_keys_do_not_match = True
                break

        for new_uri_param in new_uri_params:
            param_exists_in_both = False
            for existing_uri_param in existing_uri_params:
                if existing_uri_param == new_uri_param:
                    param_exists_in_both = True
                    break

            if not param_exists_in_both:
                param_keys_do_not_match = True
                break

        return not param_keys_do_not_match

    """
    
    """
    def find_uris_by_href(self, host, soup):
        uris = []

        for link in soup.find_all("a", href=True):
            absolute_link = self.make_absolute(host, link["href"]);
            uris.append(absolute_link)

        return uris

    """
    
    """
    def find_uris_by_forms(self, host, soup):
        uris = []

        # ToDo: add this functionality

        # inputs = soup.findAll("input", {'type':'text'})

        return uris

    """
    
    """
    def make_absolute(self, host, link):
        if link.startswith("http://") or link.startswith("https://"):
            return link

        if link.startswith("/"):
            link = link[1:]
        
        return self.get_base(host) + link

    """
    
    """
    def get_base(self, host):
        host = host.split('?')[0]

        if host.endswith("/"):
            return host

        return host + "/"

    """
    Get the contents of the given URL
    """
    def get_contents(self, url):
        return urlopen(url).read().decode("utf-8")

    """
    Get the Crawler instance
    """
    def get_instance():
        if Crawler._instance == None:
            Crawler._instance = Crawler()

        return Crawler._instance

    get_instance = staticmethod(get_instance)