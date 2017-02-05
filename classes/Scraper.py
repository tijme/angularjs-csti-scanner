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

from classes.Selenium import Selenium

"""
Get details about a particular website (like the AngularJS version etc).
"""
class Scraper:

    """
    Keep track of the Scraper instance
    """
    _instance = None

    """
    Keep track of the Scraper details
    """
    _details = {
        "uses_angular": False,
        "angular_version": None
    }

    """
    
    """
    def get_details(self, uri):
        angular_version = Selenium.get_instance().execute_js(uri, "return angular.version.full")

        self._details["uses_angular"] = angular_version != None
        self._details["angular_version"] = angular_version

        return self._details

    """
    Get the Scraper instance
    """
    def get_instance():
        if Scraper._instance == None:
            Scraper._instance = Scraper()

        return Scraper._instance

    get_instance = staticmethod(get_instance)
