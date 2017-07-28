#gi -*- coding: utf-8 -*-

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

try: # Python 3
    from urllib.parse import urlparse, parse_qsl
except: # Python 2
    from urlparse import urlparse, parse_qsl

from acstis.actions.BaseAction import BaseAction
from nyawc.helpers.URLHelper import URLHelper
from acstis.Payloads import Payloads

class QueryDataAction(BaseAction):
    """Add the payload to the GET query data from the queue item.

    Attributes:
        __payloads list(str): The payloads to add to the query data.

    """

    def __init__(self, payloads):
        """Constructs a QueryDataAction instance.

        Args:
            payloads list(str): The payloads to add to the query data.

        """

        BaseAction.__init__(self)
        self.__payloads = payloads

    def get_action_items_derived(self):
        """Get new queue items based on this action.

        Returns:
            list(:class:`nyawc.QueueItem`): A list of possibly vulnerable queue items.

        """

        items = []

        params = self.get_url_params(self.get_item().request.url)

        if not params:
            return items

        for (key, value) in params.items():
            for payload in self.__payloads:
                queue_item = self.get_item_copy()
                verify_item = self.get_item_copy()
                new_params = copy.deepcopy(params)

                new_params[key] = payload
                queue_item.payload = payload
                queue_item.request.url = self.append_with_raw_params(
                    queue_item.request.url,
                    new_params,
                    key
                )

                new_params[key] = Payloads.get_verify_payload(payload)
                verify_item.payload = Payloads.get_verify_payload(payload)
                verify_item.request.url = self.append_with_raw_params(
                    verify_item.request.url,
                    new_params,
                    key
                )

                queue_item.verify_item = verify_item
                items.append(queue_item)

        return items

    def get_url_params(self, url):
        """Get a dict of URL query parameters from the given URL.

        Args:
            url (str): The given URL to get parameters from.

        Returns:
            obj: The dict of query parameters.

        """

        parsed = urlparse(url)
        return dict(parse_qsl(parsed.query))

    def append_with_raw_params(self, url, params, raw_key):
        """Append the given URL with the given params (the param that matches the raw key will not be encoded).

        Args:
            url (str): The URL to append.
            params (obj): The parameters to append.
            raw_key (str): The parameter with this key will not be encoded.

        Returns:
            str: The new URL.

        """

        raw_value = params[raw_key]
        del params[raw_key]

        url = URLHelper.append_with_data(url.split("?")[0], params)
        url += "&" if "?" in url else "?"
        url += raw_key + "=" + raw_value

        return url
