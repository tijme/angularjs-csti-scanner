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

from sys import platform
from selenium import webdriver

import os
import ctypes

"""
The Selenium class handles everything that uses the JavaScript engine.
"""
class Selenium:

    """
    Keep track of the Selenium instance
    """
    _instance = None
        
    """
    Execute the given JavaScript code and return the response
    """
    def execute_js(self, url, command):
        browser = self.get_chrome_browser()
        browser.get(url)
            
        try:
            response = browser.execute_script(command);
        except Exception:
            response = None

        browser.close()
        return response
        
    """
    Check if the alert is really executed. Alerts could possibly not be executed because of the ngNonBindable attribute for example
    """
    def alert_is_popped(self, url):
        browser = self.get_chrome_browser()
        browser.get(url)
        
        alert_is_popped = True

        try:
            alert = browser.switch_to_alert()
            alert.accept()
        except:
            alert_is_popped = False
        
        browser.close()

        return alert_is_popped

    """
    Get the correct Chrome browser for this OS
    """
    def get_chrome_browser(self):
        chromedriver = self.get_chrome_driver()
        return webdriver.Chrome(chromedriver)

    """
    Get the correct Chrome driver for this OS
    """
    def get_chrome_driver(self):
        path = os.path.dirname(os.path.abspath(__file__))
        bits = ctypes.sizeof(ctypes.c_voidp)
        x = '32' if bits == 4 else '64'

        if platform == "linux" or platform == "linux2":
            return path + "/../chrome_drivers/chromedriver_linux" + x
        elif platform == "darwin":
            return path + "/../chrome_drivers/chromedriver_mac64"
        elif platform == "win32":
            return path + "/../chrome_drivers/chromedriver_win32"

    """
    Get the Selenium instance
    """
    def get_instance():
        if Selenium._instance == None:
            Selenium._instance = Selenium()

        return Selenium._instance

    get_instance = staticmethod(get_instance)