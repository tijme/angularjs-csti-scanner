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

        params = URLHelper.get_ordered_params(self.get_item().request.url)

        if not params:
            return items

        for (key, value) in params.items():
            for payload in self.__payloads:
                queue_item = self.get_item_copy()
                verify_item = self.get_item_copy()
                new_params = copy.deepcopy(params)

                new_params[key] = payload
                queue_item.payload = payload
                queue_item.request.url = URLHelper.append_with_data(
                    queue_item.request.url,
                    new_params
                )


                new_params[key] = Payloads.get_verify_payload(payload)
                verify_item.payload = Payloads.get_verify_payload(payload)
                verify_item.request.url = URLHelper.append_with_data(
                    verify_item.request.url,
                    new_params
                )

                queue_item.verify_item = verify_item
                items.append(queue_item)

        return items
