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

from sys import platform
from selenium import webdriver

import urllib
import json
import os
import ctypes

class Selenium:

    @staticmethod
    def execute_js(url, command):
        browser = Selenium.get_chrome_browser()
        browser.get(url)
            
        try:
            response = browser.execute_script(command);
        except Exception:
            response = None

        browser.close()
        browser.quit()
        return response

    @staticmethod
    def alert_is_popped(queue_item):
        browser = Selenium.get_chrome_browser()

        if queue_item.request.method.upper() == "POST":
            browser.get('about:blank')
            browser.execute_script('window.doRequest=function(a,b,c){c=c||"post";var d=document.createElement("form");d.setAttribute("method",c),d.setAttribute("action",a),b=decodeURIComponent(b),b=JSON.parse(b);for(var e in b)if(b.hasOwnProperty(e)){var f=document.createElement("input");f.setAttribute("type","hidden"),f.setAttribute("name",e),f.setAttribute("value",b[e]),d.appendChild(f)}document.body.appendChild(d),d.submit()}')
            browser.execute_script('window.doRequest("{}", `{}`, "{}");'.format(queue_item.request.url, urllib.parse.quote(json.dumps(queue_item.request.data)), queue_item.request.method));
        else:
            browser.get(queue_item.request.url)

        alert_is_popped = True

        try:
            alert = browser.switch_to_alert()
            alert.accept()
        except Exception as err:
            alert_is_popped = False
        
        browser.close()
        browser.quit()

        return alert_is_popped

    @staticmethod
    def get_chrome_browser():
        chromedriver = Selenium.get_chrome_driver()
        return webdriver.Chrome(chromedriver)

    @staticmethod
    def get_chrome_driver():
        path = os.path.dirname(os.path.abspath(__file__))
        bits = ctypes.sizeof(ctypes.c_voidp)
        x = '32' if bits == 4 else '64'

        if platform == "linux" or platform == "linux2":
            return path + "/chrome_drivers/chromedriver_linux" + x
        elif platform == "darwin":
            return path + "/chrome_drivers/chromedriver_mac64"
        elif platform == "win32":
            return path + "/chrome_drivers/chromedriver_win32"