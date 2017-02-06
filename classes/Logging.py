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

from colorama import Fore, Back, Style

import datetime

"""
A simple helper for logging messages to the console (including timestamp)
"""
class Logging:

    """
    Log white text with a black background to the console
    """
    def info(message):
        print(Back.BLACK + str(datetime.datetime.now()) + ": " + message);

    info = staticmethod(info)

    """
    Log red text with a black background to the console
    """
    def red(message):
        print(Fore.RED + Back.BLACK + str(datetime.datetime.now()) + ": " + message);

    red = staticmethod(red)

    """
    Log green text with a black background to the console
    """
    def green(message):
        print(Fore.GREEN + Back.BLACK + str(datetime.datetime.now()) + ": " + message);

    """
    Log yellow text with a black background to the console
    """
    def yellow(message):
        print(Fore.YELLOW + Back.BLACK + str(datetime.datetime.now()) + ": " + message);

    green = staticmethod(green)
