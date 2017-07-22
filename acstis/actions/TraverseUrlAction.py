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

from acstis.actions.BaseAction import BaseAction
from acstis.Payloads import Payloads

class TraverseUrlAction(BaseAction):
    """Traverse the payload in the URL from the queue item.

    Attributes:
        __payloads list(str): The payloads to traverse in the URL.

    """

    def __init__(self, payloads):
        """Constructs a TraverseUrlAction instance.

        Args:
            payloads list(str): The payloads to traverse in the URL.

        """

        BaseAction.__init__(self)
        self.__payloads = payloads

    def get_action_items_derived(self):
        """Get new queue items based on this action.

        Returns:
            list(:class:`nyawc.QueueItem`): A list of possibly vulnerable queue items.

        """

        items = []

        path = self.get_parsed_url().path
        filename = self.get_filename()

        if filename:
            path[0:-len(filename)]

        parts = list(filter(None, path.split("/")))

        for index in range(0, len(parts)):
            for payload in self.__payloads:
                queue_item = self.get_item_copy()
                verify_item = self.get_item_copy()
                path = "/".join(parts[0:index])

                path_with_affix = ("/" if path else "") + path + "/" + payload
                parsed = self.get_parsed_url(queue_item.request.url)
                parsed = parsed._replace(path=path_with_affix, query="")
                queue_item.request.url = parsed.geturl()
                queue_item.payload = payload

                path_with_affix = ("/" if path else "") + path + "/" + Payloads.get_verify_payload(payload)
                parsed = self.get_parsed_url(verify_item.request.url)
                parsed = parsed._replace(path=path_with_affix, query="")
                verify_item.request.url = parsed.geturl()
                verify_item.payload = Payloads.get_verify_payload(payload)

                queue_item.verify_item = verify_item
                items.append(queue_item)

        return items
