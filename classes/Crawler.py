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
from classes.Logging import Logging

import sys 

"""

"""
class Crawler:

    """
    Keep track of the Crawler instance
    """
    _instance = None

    """
    Keep track of all the crawled URI's
    """
    _uris = []

    """
    
    """
    def get_urls(self, uri):
        self.crawl_uris_recursively(uri)

        found_uris = []
        for crawled_uri in self._uris:
            found_uris.append(crawled_uri["uri"])

        found_uris.append(uri)
        found_uris.append(uri + "?canonical=check")
        found_uris.append(uri + "&canonical=check")

        return found_uris

    """

    """
    def crawl_uris_recursively(self, uri, force=False):
        if self.has_crawled_uri(uri) and not force:
            return

        Logging.yellow("Crawling URL: {}".format(uri))

        contents = self.get_contents(uri)
        soup = BeautifulSoup(contents, "html.parser")

        uris_by_href = self.find_uris_by_href(uri, soup)
        self._uris = self.merge_uris_without_duplicates(uri, self._uris, uris_by_href)        

        uris_by_forms = self.find_uris_by_forms(uri, soup)
        self._uris = self.merge_uris_without_duplicates(uri, self._uris, uris_by_forms)

        for crawled_uri in self._uris:
            if crawled_uri["crawled"] is False:
                crawled_uri["crawled"] = True
                self.crawl_uris_recursively(crawled_uri["uri"], True)
                break

    """

    """
    def has_crawled_uri(self, uri):
        for crawled_uri in self._uris:
            if crawled_uri["uri"] == uri:
                return True

        return False

    """
    
    """
    def merge_uris_without_duplicates(self, uri, existing_uris, new_uris):
        for new_uri in new_uris:
            already_in = False
            for existing_uri in existing_uris:
                if self.url_is_essentially_the_same(existing_uri["uri"], new_uri):
                    already_in = True
                    break

            if not already_in and self.get_hostname(uri) == self.get_hostname(new_uri):
                existing_uris.append({
                    "uri": new_uri,
                    "crawled": False
                })

        return existing_uris

    """
    Get the hostname of the given URL
    """
    def get_hostname(self, url):
        parsed = urlparse(url)
        return parsed.netloc

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

        if self.get_base(existing_uri, True) != self.get_base(new_uri, True):
            return False

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

        for form in soup.find_all("form"):
            uris.append(self.find_uri_by_form(host, form))

        return uris

    """
    
    """
    def find_uri_by_form(self, host, form):
        url = form.get("action")
        if len(url) is 0:
            url = host

        url = self.make_absolute(host, url).split('?')[0] + "?a=b"

        inpts = form.find_all("input", {"type": ["text", "hidden"]})
        for inpt in inpts:
            url = url + "&{}={}".format(inpt.get("name"), inpt.get("value"))

        selects = form.find_all("select")
        for select in selects:
            name = select.get("name")
            value = self.get_select_value(select)
            url = url + "&{}={}".format(name, value)

        return url

    """
    
    """
    def get_select_value(self, select):
        selected = select.find("option", selected=True)
        if selected is not None:
            return selected.get("value")

        first = select.find("option")
        if first is not None:
            return first.get("value")

        return "not-found"

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
    def get_base(self, host, include_file=False):
        if include_file:
            host = host.split('?')[0]
        else:
            host = host.rsplit('/', 1)[0]

        if host.endswith("/") or include_file:
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