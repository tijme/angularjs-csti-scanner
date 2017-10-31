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
import subprocess

from nyawc.QueueItem import QueueItem
from nyawc.http.Request import Request
from nyawc.http.Response import Response
from acstis.helpers.BrowserHelper import BrowserHelper
from test.tools.LocalAngularServer import LocalAngularServer

class TestAngularScope(unittest.TestCase):
    """The TestAngularScope class checks if payloads are detected correctly (without using PhantomJS)."""

    def test_inside_app(self):
        """Payloads inside the AngularJS app should be detected."""

        server = LocalAngularServer()
        server.start(LocalAngularServer.HANDLER_SCOPE_TEST, {"position": "inside_app"})

        try:
            shell_command = ["python", "acstis.py", "--verify-payload", "--domain", "http://" + server.url + "?vulnerable=payload"]

            process = subprocess.Popen(
                shell_command
            )

            exitcode = process.wait()
        except Exception as e:
            print("Exception: " + str(e))
            exitcode = 1

        server.stop()

        self.assertEqual(exitcode, 0)

    def test_outside_app(self):
        """Payloads outside the AngularJS app shouldn't be detected."""

        server = LocalAngularServer()
        server.start(LocalAngularServer.HANDLER_SCOPE_TEST, {"position": "outside_app"})

        try:
            shell_command = ["python", "acstis.py", "--verify-payload", "--domain", "http://" + server.url + "?vulnerable=payload"]

            process = subprocess.Popen(
                shell_command
            )

            exitcode = process.wait()
        except Exception as e:
            print("Exception: " + str(e))
            exitcode = 1

        server.stop()

        self.assertNotEqual(exitcode, 0)

    def test_inside_non_bindable(self):
        """Payloads inside the non bindable attributes shouldn't be detected."""

        server = LocalAngularServer()
        server.start(LocalAngularServer.HANDLER_SCOPE_TEST, {"position": "inside_non_bindable"})

        try:
            shell_command = ["python", "acstis.py", "--verify-payload", "--domain", "http://" + server.url + "?vulnerable=payload"]

            process = subprocess.Popen(
                shell_command
            )

            exitcode = process.wait()
        except Exception as e:
            print("Exception: " + str(e))
            exitcode = 1

        server.stop()

        self.assertNotEqual(exitcode, 0)

    def test_inside_script(self):
        """Payloads inside a script tag shouldn't be detected."""

        server = LocalAngularServer()
        server.start(LocalAngularServer.HANDLER_SCOPE_TEST, {"position": "inside_script"})

        try:
            shell_command = ["python", "acstis.py", "--verify-payload", "--domain", "http://" + server.url + "?vulnerable=payload"]

            process = subprocess.Popen(
                shell_command
            )

            exitcode = process.wait()
        except Exception as e:
            print("Exception: " + str(e))
            exitcode = 1

        server.stop()

        self.assertNotEqual(exitcode, 0)
