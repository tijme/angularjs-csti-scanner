# AngularJS sandbox escape/bypass scanner

*Automated client-side template injection (CSTI) detection for AngularJS!*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)

## Demo
[![Demo](https://finnwea.com/snippets/angularjs-sandbox-escape-scanner.gif)](https://finnwea.com/snippets/angularjs-sandbox-escape-scanner.gif) 
*Click for looped GIF*

## Installation

Install [Python 3](https://www.python.org/downloads/) and the requirements.

`pip install -r requirements.txt`

## Usage

### Options
`python angular.py [options]`
* `-u <uri>`,      `--uri=<uri>`              (required)        The URI to run the exploit on (e.g. https://www.example.ltd/?vulnerable=param).
* `-v`,            `--verify`                 (optional)        Extra check by a JavaScript engine to ensure the payload is executed.
* `-h`,            `--help`                   (optional)        Print this help message.

### Examples

**Print a help message:**

`python angular.py --help`

**Check a single URI:**

`python angular.py --uri="http://example.ltd/some/page?test1=a&test2=b&test3=c"`

**Check a single URI and use a JavaScript engine to ensure the alert really pops:**

`python angular.py --uri="http://example.ltd/some/page?test1=a&test2=b&test3=c" --verify`

**Crawl the whole website and check all URI's for AngularJS sandbox escape:**

~~`python angular.py --uri="http://example.ltd/" --crawl`~~ **(coming soon)**

**Stop checking all the URI's if a vulnerable was found:**

~~`python angular.py --uri="http://example.ltd/" --crawl --quit-if-vulnerable`~~ **(coming soon)**

## ToDo

1. Use Selenium headless (maybe using PhantomJS).
2. Add support for cookies and basic auth.
3. Add support for custom user agents.
4. Add support for SEO url injection.
5. Create the crawler (including support for POST requests).
6. Document all code.