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

import copy

from nyawc.QueueItem import QueueItem
from nyawc.http.Request import Request
from nyawc.http.Response import Response

try: # Python 3
    from urllib.parse import urljoin, urlparse, parse_qsl, urlencode, urlunparse
except: # Python 2
    from urllib import urlencode
    from urlparse import urljoin, urlparse, parse_qsl, urlunparse

class BaseAction(object):
    """The BaseAction can be used to create other actions.

    Attributes:
        __queue_item (:class:`nyawc.QueueItem`): The queue item containing the response to scrape.

    """

    def get_action_items(self, queue_item):
        """Get new queue items that could be vulnerable.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item containing a response the scrape.

        Returns:
            list(:class:`nyawc.QueueItem`): A list of new queue items that were found.

        """

        self.__queue_item = queue_item
        return self.get_action_items_derived()

    def get_item(self):
        """Get the original queue item.

        Returns:
            :class:`nyawc.QueueItem`: The original queue item.

        """

        return self.__queue_item

    def get_item_copy(self):
        """Copy the current queue item.

        Returns:
            :class:`nyawc.QueueItem`: A copy of the current queue item.

        """

        request = copy.deepcopy(self.__queue_item.request)
        return QueueItem(request, Response(request.url))

    def get_parsed_url(self, url=None):
        """Get the parsed URL.

        Args:
            url (str): The URL to parse (None will use the queue item URL)

        Returns:
            ParseResult: The parsed URL.

        """

        if url:
            return urlparse(url)

        if not hasattr(self.__queue_item.request, 'url_parsed'):
            url_parsed = urlparse(self.__queue_item.request.url)
            self.__queue_item.request.url_parsed = url_parsed

        return self.__queue_item.request.url_parsed

    def get_filename(self):
        """Get the filename from the current queue item URL, if exists.

        Returns:
            str: The filename, or None if it does not exist.

        """

        filename = self.get_parsed_url().path.split("/")[-1]

        if "." in filename:
            return filename

        return None

    def get_extension(self):
        """Get the extension from the current queue item URL, if exists.

        Returns:
            str: The extension, or None if it does not exist.

        """

        filename = self.get_filename()

        if filename:
            return filename.split(".")[-1]

        return None

    def replace_filename(self, url, to_replace):
        """Replace the filename in the URL with the given ``to_replace``.

        Args:
            url (str): The URL to update.
            to_replace (str): The new affix.

        Returns:
            str: The new URL.

        """

        filename = self.get_filename()
        without_filename = url[0:-len(filename)]

        return without_filename + to_replace

    def append_filename(self, url, to_append):
        """Append the URL with the given ``to_append``.

        Args:
            url (str): The URL to append.
            to_append (str): The new affix.

        Returns:
            str: The new URL.

        """

        parsed = self.get_parsed_url(url)
        path = parsed.path

        if not path or path[-1] != "/":
            path += "/"

        new_path = path + to_append

        parsed = parsed._replace(path=new_path)
        return parsed.geturl()
