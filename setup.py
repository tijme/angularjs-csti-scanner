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

from setuptools import find_packages, setup

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(
    version ="2.0.5",   
    name = "acstis",
    description = "Automated client-side template injection (CSTI, sandbox escape/bypass) detection for AngularJS!",
    long_description = "",
    keywords = "angularjs xss xss-scanner exploit angularjs-sandbox-escape vulnerability-scanner",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.3",
        "Topic :: Security"
    ],
    packages = find_packages(),
    platforms = ["any"],
    author = "Tijme Gommers",
    author_email ="tijme@finnwea.com",
    license = "MIT",
    url = "https://github.com/tijme/angularjs-csti-scanner",
    install_requires = requirements,
    entry_points = {
        'console_scripts': [
            'acstis = scripts.acstis_cli:main'
        ]
    },
    package_data={
        'acstis': [
            'chrome_drivers/chromedriver_linux32',
            'chrome_drivers/chromedriver_linux64',
            'chrome_drivers/chromedriver_mac64',
            'chrome_drivers/chromedriver_win32.exe'
        ]
    }
)
