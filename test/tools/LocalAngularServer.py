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

class LocalAngularServer:
    """The LocalAngularServer class sets up a local vulnerable AngularJS server.

    Attributes:
        running (bool): If the thread should keep running.
        sock (obj): A reference to the socket.
        asset (str): A URL to the AngularJS asset to use.
        thread (obj): A reference to the thread.
        url (str): The URL to the local server.

    """

    def start(self, asset):
        """Start the websocket to accept HTTP request on localhost.

        Args:
            asset (str): A URL to the AngularJS asset to use.

        """

        self.running = True
        self.asset = asset

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("0.0.0.0", 0))
        self.sock.listen(1)

        self.thread = threading.Thread(target=self.__handler)
        self.thread.start()

        self.url = self.sock.getsockname()[0] + ":" + str(self.sock.getsockname()[1])

    def __handler(self):
        """Serve a vulnerable AngularJS application for every HTTP request."""

        try:
            while self.running:
                csock, caddr = self.sock.accept()
                request = csock.recv(1024)

                matches = re.findall(r'GET \/\?vulnerable=(.*) HTTP', request.decode("utf-8"))
                vulnerableValue = matches[0] if len(matches) == 1 else ""

                html = """
                    <!DOCTYPE html>
                    <html>
                        <head>
                            <title>1.0.4</title>
                            <script src='""" + self.asset + """'></script>
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
            print(e)

    def stop(self):
        """Stop the websocket."""

        self.running = False
        self.sock.close()
        self.thread.join()
