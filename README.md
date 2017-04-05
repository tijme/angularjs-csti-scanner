<p align="center">
    <img src="https://github.com/tijme/angular-csti-scanner/blob/develop/.github/logo.png" height="300" alt="AngularJS CSTI Scanner">
    <br/>
    <a href="https://www.python.org/"><img src="https://img.shields.io/pypi/pyversions/acstis.svg" alt="Python version"></a>
    <a href="https://pypi.python.org/pypi/acstis/"><img src="https://img.shields.io/pypi/v/acstis.svg" alt="PyPi version"></a>
    <a href="LICENSE.md"><img src="https://img.shields.io/pypi/l/acstis.svg" alt="License: MIT"></a>
</p>

## AngularJS CSTI Scanner

AngularJS CSTI Scanner (ACSTIS) is a Python application that enables you to scan certain web applications for AngularJS Client Side Template Injection (CSTI, sandbox escape/bypass). It supports scanning a single request but also crawling an entire web application for the vulnerability.

## Installation
First make sure you're on [Python 3.3](https://www.python.org/) or higher. Then run the command below to install ACSTIS.

`pip install --upgrade acstis`

## Usage

### Options
`python acstis.py [options]`
* `-u <uri>`,      `--uri=<uri>`              (required)        The URI to run the exploit on (e.g. https://www.example.ltd/?vulnerable=param).
* `-v`,            `--verify`                 (optional)        Extra check by a JavaScript engine to ensure the payload is executed.
* `-h`,            `--help`                   (optional)        Print this help message.

### Examples

**Print a help message:**

`python acstis.py --help`

**Check a single URI:**

`python acstis.py --uri="http://example.ltd/some/page?test1=a&test2=b&test3=c"`

**Check a single URI and use a JavaScript engine to ensure the alert really pops:**

`python acstis.py --uri="http://example.ltd/some/page?test1=a&test2=b&test3=c" --verify`

**Crawl the whole website and check all URI's for AngularJS sandbox escape:**

`python acstis.py --uri="http://example.ltd/" --crawl`

**Stop checking all the URI's if a vulnerable was found:**

`python acstis.py --uri="http://example.ltd/" --crawl --quit-if-vulnerable`

## ToDo

1. Use Selenium headless (maybe using PhantomJS).
2. Add support for cookies and basic auth.
3. Add support for SEO url injection.
4. Document all code.
