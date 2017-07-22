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

class FormDataAction(BaseAction):
    """Add the payload to the POST form data from the queue item.

    Attributes:
        __payloads list(str): The payloads to add to the form data.

    """

    def __init__(self, payloads):
        """Constructs a FormDataAction instance.

        Args:
            payloads list(str): The payloads to add to the form data.

        """

        BaseAction.__init__(self)
        self.__payloads = payloads

    def get_action_items_derived(self):
        """Get new queue items based on this action.

        Returns:
            list(:class:`nyawc.QueueItem`): A list of possibly vulnerable queue items.

        """

        items = []

        if not self.get_item().request.data:
            return items

        for (key, value) in self.get_item().request.data.items():
            for payload in self.__payloads:
                queue_item = self.get_item_copy()
                verify_item = self.get_item_copy()

                queue_item.request.data[key] = payload
                queue_item.payload = payload

                verify_item.request.data[key] = Payloads.get_verify_payload(payload)
                verify_item.payload = Payloads.get_verify_payload(payload)

                queue_item.verify_item = verify_item
                items.append(queue_item)

        return items
