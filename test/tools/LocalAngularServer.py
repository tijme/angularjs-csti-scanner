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

import re
import socket
import threading

try: # Python 3
    from urllib.parse import unquote
except: # Python 2
    from urllib import unquote

class LocalAngularServer:
    """The LocalAngularServer class sets up a local vulnerable AngularJS server.

    Attributes:
        running (bool): If the thread should keep running.
        sock (obj): A reference to the socket.
        data (str): An object with extra data for the handler.
        thread (obj): A reference to the thread.
        url (str): The URL to the local server.
        HANDLER_VULNERABLE_TEST (str): A handler for testing vulnerable applications.
        HANDLER_SCOPE_TEST (str): A handler for testing payloads in certain scopes.

    """

    HANDLER_VULNERABLE_TEST = "handler_vulnerable_test"

    HANDLER_SCOPE_TEST = "handler_scope_test"

    def start(self, handler, data):
        """Start the websocket to accept HTTP request on localhost.

        Args:
            handler (str): The response handler to use.
            data (obj): An object with extra data for the handler.

        """

        self.running = True
        self.data = data

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(30)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(1)

        self.thread = threading.Thread(target=getattr(self, handler))
        self.thread.start()

        self.url = "127.0.0.1:" + str(self.sock.getsockname()[1])

    def handler_vulnerable_test(self):
        """Serve a vulnerable AngularJS application for every HTTP request."""

        try:
            while self.running:
                csock, caddr = self.sock.accept()
                request = csock.recv(1024)

                matches = re.findall(r'GET \/\?vulnerable=(.*) HTTP', request.decode("utf-8"))
                vulnerableValue = unquote(matches[0])  if len(matches) == 1 else ""

                html = """
                    <!DOCTYPE html>
                    <html>
                        <head>
                            <script src='""" + self.data["asset"] + """'></script>
                        </head>
                        <body ng-app="">
                            <a href="?vulnerable=payload">Payload</a>
                            """ + vulnerableValue + """
                        </body>
                    </html>
                """

                csock.sendall(b"""HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n""" + bytes(html.encode("UTF-8")))
                csock.close()
        except Exception as e:
            self.running = False

    def handler_scope_test(self):
        """Serve a vulnerable AngularJS application for every HTTP request."""

        try:
            while self.running:
                csock, caddr = self.sock.accept()
                request = csock.recv(1024)

                matches = re.findall(r'GET \/\?vulnerable=(.*) HTTP', request.decode("utf-8"))
                vulnerableValue = unquote(matches[0])  if len(matches) == 1 else ""

                inside_app = vulnerableValue if self.data["position"] == "inside_app" else ""
                outside_app = vulnerableValue if self.data["position"] == "outside_app" else ""
                inside_non_bindable = vulnerableValue if self.data["position"] == "inside_non_bindable" else ""
                inside_script = vulnerableValue if self.data["position"] == "inside_script" else ""

                html = """
                    <!DOCTYPE html>
                    <html>
                        <head>
                            <script src='https://code.angularjs.org/1.5.8/angular.min.js'></script>
                        </head>
                        <body>
                            <a href="?vulnerable=payload">Payload</a>
                            <div ng-app="">
                                """ + inside_app + """
                                <p ng-non-bindable><span>""" + inside_non_bindable + """</span></p>
                                <script>""" + inside_script + """</script>
                            </div>
                            """ + outside_app + """
                        </body>
                    </html>
                """

                csock.sendall(b"""HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n""" + bytes(html.encode("UTF-8")))
                csock.close()
        except Exception as e:
            self.running = False

    def stop(self):
        """Stop the websocket."""

        self.running = False
        self.sock.close()
        self.thread.join()
