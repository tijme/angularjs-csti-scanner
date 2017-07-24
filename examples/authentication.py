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

from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from nyawc.Options import Options
from acstis.Driver import Driver, Namespace

if __name__ == "__main__":
    """Start ACSTIS using BasicAuth as authentication.

    Note:
        Please check https://tijme.github.io/not-your-average-web-crawler/latest/options_crawling_identity.html#authentication for all
        the authentication options and explanations.

    """

    options = Options()

    #options.identity.auth = HTTPDigestAuth("username", "password")
    options.identity.auth = HTTPBasicAuth("username", "password")

    driver = Driver(Namespace(
        domain="https://finnwea.com",
        verify_payload=False
    ), options)

    driver.start()
