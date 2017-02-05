# AngularJS sandbox escape/bypass scanner

**Under development**

*Automated client-side template injection (CSTI) detection for AngularJS!*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)

## Dependencies
* Python 3: https://www.python.org/downloads/
* BeautifulSoup: `pip install -U beautifulsoup4`
* Selenium: `pip install -U selenium`
* Colorama: `pip install -U colorama`

## Usage

### Options
`python angular.py [options]`
* `-u <uri>`,      `--uri=<uri>`              (required)        The hostname or URL to run the exploit on (e.g. https://www.example.ltd/).
* `-v`,            `--verify`                 (optional)        Extra check by a JavaScript engine to ensure the payload is executed.
* `-c`,            `--crawl`                  (optional)        Crawl & test all available URL's on the hostname of the given URL.
* `-q`,            `--quit-if-vulnerable`     (optional)        Stop testing if a vulnerable URL was found.
* `-h`,            `--help`                   (optional)        Print this help message.

### Examples

**Print a help message:**

`python angular.py --help`

**Check a single URI:**

`python angular.py --uri="http://example.ltd/some/page?test1=a&test2=b&test3=c"`

**Check a single URI and use a JavaScript engine to ensure the alert really pops:**

`python angular.py --uri="http://example.ltd/some/page?test1=a&test2=b&test3=c" --verify`

**Crawl the whole website and check all URI's for AngularJS sandbox escape:**

`python angular.py --uri="http://example.ltd/" --crawl`

**Stop checking all the URI's if a vulnerable was found:**

`python angular.py --uri="http://example.ltd/" --crawl --quit-if-vulnerable`

## ToDo

1. Add a payload for AngularJS v1.3.0.
2. Add a payload for AngularJS v1.5.9 to v1.5.11.
3. Add the crawler functionality.
4. Use Selenium headless.
5. Add docblocks for all methods.
6. Catch Selenium exceptions.