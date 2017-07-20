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

        return items
