# AngularJS sandbox escape/bypass scanner
*Automated client-side template injection detection for AngularJS!*

## Dependencies
* Python 3: https://www.python.org/downloads/
* BeautifulSoup: `pip install -U beautifulsoup4`
* Selenium: `pip install -U selenium`

## Usage

### Options
`python angular.py [options]`
* `-u <http_host>` or `--url=<http_host>`: The website to run the exploit on (e.g. https://www.example.ltd).
* `-j` or `--javascript-engine`: Extra check by a JavaScript engine to ensure the payload is executed.
* `-h` or `--help`: Print a help message.

### Examples

**Simple check:**

`python angular.py --url="http://example.ltd/"`

**Also use a JavaScript engine to ensure the alert really pops:**

`python angular.py --url="http://example.ltd/" --javascript-engine`
