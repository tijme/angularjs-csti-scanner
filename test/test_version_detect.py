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

import unittest

from nyawc.QueueItem import QueueItem
from nyawc.http.Request import Request
from nyawc.http.Response import Response
from acstis.helpers.BrowserHelper import BrowserHelper
from test.tools.LocalAngularServer import LocalAngularServer

class TestVersionDetect(unittest.TestCase):
    """The TestVersionDetect class checks if the AngularJS versions are detected correctly."""

    def test_version_detect(self):
        """Check if a single (stable) AngularJS version is detected by ACSTIS."""

        server = LocalAngularServer()
        server.start(LocalAngularServer.HANDLER_VULNERABLE_TEST, {"asset": "https://code.angularjs.org/1.5.8/angular.min.js"})

        domain = "http://" + server.url + "?vulnerable=payload"

        version = BrowserHelper.javascript(
            QueueItem(Request(domain), Response(domain)),
            "return angular.version.full"
        )

        server.stop()

        self.assertEqual("1.5.8", version)
