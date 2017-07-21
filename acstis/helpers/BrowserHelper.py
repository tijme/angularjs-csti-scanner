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

import os
import sys
import ctypes
import colorlog

from selenium import webdriver

class BrowserHelper:
    """The BrowserHelper enables headless web browsing."""

    @staticmethod
    def javascript(url, command):
        """Execute a JavaScript command on the given URL.

        Args:
            url (str): URL to navigate to and execute the JavaScript on.
            command (str): The JavaScript command.

        Returns:
            str: The response of the JavaScript command.

        """

        try:
            browser = BrowserHelper.__get_browser()
            browser.get(url)
            response = browser.execute_script(command)
            browser.quit()
        except Exception as e:
            response = None

        return response

    @staticmethod
    def __get_browser():
        """Get the PhantomJS browser.

        Returns:
            obj: The PhantomJS Selenium object.

        """

        driver = BrowserHelper.__get_phantomjs_driver()
        return webdriver.PhantomJS(executable_path=driver)

    @staticmethod
    def __get_phantomjs_driver():
        """Get the path to the correct PhantomJS driver.

        Returns:
            str: The location of the driver.

        """

        path = os.path.dirname(os.path.abspath(__file__))
        bits = ctypes.sizeof(ctypes.c_voidp)
        x = '32' if bits == 4 else '64'

        if sys.platform == "linux" or sys.platform == "linux2":
            return path + "/../phantomjs/linux" + x + "-2.1.1"
        elif sys.platform == "darwin":
            return path + "/../phantomjs/mac-2.1.1"
        elif sys.platform == "win32":
            return path + "/../phantomjs/win-2.1.1"
