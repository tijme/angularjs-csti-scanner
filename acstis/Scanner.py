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

import requests

from acstis.Payloads import Payloads
from acstis.actions.TraverseUrlAction import TraverseUrlAction
from acstis.actions.FormDataAction import FormDataAction
from acstis.actions.QueryDataAction import QueryDataAction

class Scanner:
    """The BaseAction can be used to create other actions.

    Attributes:
        scanned_hashes list(str): A list of scanned queue item hashes.
        __actions list(:class:`acstis.actions.BaseAction`): The actions to perform on the queue item.
        __driver (:class:`acstis.Driver`): Used to check if we should stop scanning.
        __queue_item (:class:`nyawc.QueueItem`): The queue item to perform actions on.
        __session (obj): A Python requests session.

    """

    scanned_hashes = []

    def __init__(self, driver, angular_version, queue_item):
        """Initialize a scanner for the given queue item.

        Args:
            driver (:class:`acstis.Driver`): Used to check if we should stop scanning.
            angular_version (str): The AngularJS version of the given queue_item (e.g. `1.4.2`).
            queue_item (:class:`nyawc.QueueItem`): The queue item to scan.

        """

        self.__driver = driver
        self.__queue_item = queue_item
        self.__session = requests.Session()

        self.__session.mount('http://', requests.adapters.HTTPAdapter(max_retries=2))
        self.__session.mount('https://', requests.adapters.HTTPAdapter(max_retries=2))

        self.__actions = [
            TraverseUrlAction(Payloads.get_for_version(angular_version)),
            FormDataAction(Payloads.get_for_version(angular_version)),
            QueryDataAction(Payloads.get_for_version(angular_version))
        ]

    def get_vulnerable_items(self):
        """Get a list of vulnerable queue items, if any.

        Returns:
            list(:class:`nyawc.QueueItem`): A list of vulnerable queue items.

        """

        results = []

        for action in self.__actions:
            if self.__driver.stopping:
                break

            items = action.get_action_items(self.__queue_item)

            for item in items:
                if self.__driver.stopping:
                    break

                if item.get_hash() in self.scanned_hashes:
                    continue

                self.scanned_hashes.append(item.get_hash())

                if self.is_item_vulnerable(item):
                    results.append(item)

        return results

    def is_item_vulnerable(self, queue_item):
        """Check if the given queue item is vulnerable by executing it using the HttpHandler.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item to check.

        Returns:
            bool: True if vulnerable, false otherwise.

        """

        try:
            queue_item.response = self.__make_request(
                queue_item.request.url,
                queue_item.request.method,
                queue_item.request.data,
                queue_item.request.auth,
                queue_item.request.cookies,
                queue_item.request.headers,
                queue_item.request.proxies,
                15
            )

            try:
                queue_item.response.raise_for_status()
            except Exception:
                return False

        except Exception:
            return False

        return True


    def __make_request(self, url, method, data, auth, cookies, headers, proxies, timeout):
        """Execute a request with the given data.

        Args:
            url (str): The URL to call.
            method (str): The method (e.g. `get` or `post`).
            data (str): The data to call the URL with.
            auth (obj): The authentication class.
            cookies (obj): The cookie dict.
            headers (obj): The header dict.
            proxies (obj): The proxies dict.
            timeout (int): The request timeout in seconds

        Returns:
            obj: The response object.

        """

        request_by_method = getattr(self.__session, method)
        return request_by_method(
            url=url,
            data=data,
            auth=auth,
            cookies=cookies,
            headers=headers,
            proxies=proxies,
            timeout=timeout,
            allow_redirects=True,
            stream=False
        )
