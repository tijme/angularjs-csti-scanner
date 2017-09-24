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
import json
import stat
import ctypes
import colorlog
import requests.cookies

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from nyawc.helpers.HTTPRequestHelper import HTTPRequestHelper
from nyawc.helpers.URLHelper import URLHelper
from nyawc.http.Request import Request

try: # Python 3
    from urllib.parse import quote, urlparse
except: # Python 2
    from urllib import quote
    from urlparse import urlparse

class BrowserHelper:
    """The BrowserHelper enables headless web browsing.

    Attributes:
        __phantomjs_driver (str): The cached path to the executable PhantomJS driver.

    """

    __phantomjs_driver = None

    @staticmethod
    def request(queue_item):
        """Execute the given queue item and return the browser instance.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item to execute the JavaScript on.

        Returns:
            obj: The browser instance reference.

        """

        try:
            browser = BrowserHelper.__get_browser(queue_item)

            if queue_item.request.method == Request.METHOD_POST:
                browser.get('about:blank')
                browser.execute_script('window.doRequest=function(a,b,c){c=c||"post";var d=document.createElement("form");d.setAttribute("method",c),d.setAttribute("action",a),b=decodeURIComponent(b),b=JSON.parse(b);for(var e in b)if(b.hasOwnProperty(e)){var f=document.createElement("input");f.setAttribute("type","hidden"),f.setAttribute("name",e),f.setAttribute("value",b[e]),d.appendChild(f)}document.body.appendChild(d),d.submit()}')
                browser.execute_script('window.doRequest("{}", `{}`, "{}");'.format(queue_item.request.url, quote(json.dumps(queue_item.request.data)), queue_item.request.method));
            else:
                browser.get(queue_item.request.url)

            return browser
        except Exception as e:
            return None

    @staticmethod
    def javascript(queue_item, command):
        """Execute a JavaScript command on the given queue item.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item to execute the JavaScript on.
            command (str): The JavaScript command.

        Returns:
            str: The response of the JavaScript command.

        """

        try:
            browser = BrowserHelper.request(queue_item)
            response = browser.execute_script(command)
            browser.quit()
        except Exception as e:
            response = None

        return response

    @staticmethod
    def __get_browser(queue_item=None):
        """Get the PhantomJS browser.

        Args:
            queue_item (:class:`nyawc.QueueItem`): Use authentication/headers/cookies etc from this queue item (if given).

        Returns:
            obj: The PhantomJS Selenium object.

        """

        capabilities = dict(DesiredCapabilities.PHANTOMJS)
        service = []

        if queue_item:

            # Add authentication header to request
            if queue_item.request.auth:
                queue_item.request.auth(queue_item.request)

            # Add cookie header to request
            if queue_item.request.cookies:
                cookie_string = HTTPRequestHelper.get_cookie_header(queue_item)
                queue_item.request.headers["Cookie"] = cookie_string

            # Add headers to PhantomJS
            if queue_item.request.headers:
                for (key, value) in queue_item.request.headers.items():
                    if key.lower() == "user-agent":
                        capabilities["phantomjs.page.settings.userAgent"] = value
                    else:
                        print(key + " === " + value)
                        capabilities["phantomjs.page.settings." + key] = value
                        capabilities["phantomjs.page.customHeaders." + key] = value

            # Proxies
            if queue_item.request.proxies:
                service.extend(BrowserHelper.__proxies_to_service_args(queue_item.request.proxies))

        driver_path = BrowserHelper.__get_phantomjs_driver()
        return webdriver.PhantomJS(
            executable_path=driver_path,
            desired_capabilities=capabilities,
            service_args=service
        )

    @staticmethod
    def __proxies_to_service_args(proxies):
        """Get the proxy details in a service args array.

        Args:
            proxies (obj): An `requests` proxies object.

        Returns:
            list: The service args containing proxy details

        Note:
            The `ignore-ssl-errors` argument is also added because
            all SSL checks are handled by Python's requests module.
            Python's requests module is also able to allow certain
            custom certificates (e.g. if a proxy is used).

        """

        service_args = []

        parsed = urlparse(list(proxies.values())[0])

        # Proxy type
        if parsed.scheme.startswith("http"):
            service_args.append("--proxy-type=http")
        else:
            service_args.append("--proxy-type=" + parsed.scheme)

        # Proxy
        host_and_port = parsed.netloc.split("@")[-1]
        service_args.append("--proxy=" + host_and_port)

        # Proxy auth
        if len(parsed.netloc.split("@")) == 2:
            user_pass = parsed.netloc.split("@")[0]
            service_args.append("--proxy-auth=" + user_pass)

        # Ignore SSL (please see note in this method).
        service_args.append("--ignore-ssl-errors=true")

        return service_args

    @staticmethod
    def __get_phantomjs_driver():
        """Get the path to the correct PhantomJS driver.

        Returns:
            str: The location of the driver.

        """

        if BrowserHelper.__phantomjs_driver:
            return BrowserHelper.__phantomjs_driver

        path = os.path.dirname(os.path.abspath(__file__))
        bits = ctypes.sizeof(ctypes.c_voidp)
        x = "32" if bits == 4 else "64"

        if sys.platform == "linux" or sys.platform == "linux2":
            file = path + "/../phantomjs/linux" + x + "-2.1.1"
        elif sys.platform == "darwin":
            file =  path + "/../phantomjs/mac-2.1.1"
        elif sys.platform == "win32":
            file =  path + "/../phantomjs/win-2.1.1.exe"

        st = os.stat(file)
        os.chmod(file, st.st_mode | stat.S_IEXEC)

        BrowserHelper.__phantomjs_driver = file
        return BrowserHelper.__phantomjs_driver
