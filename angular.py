#!/usr/bin/env python

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

from classes.Crawler import Crawler
from classes.Exploit import Exploit
from classes.Logging import Logging
from classes.Scraper import Scraper
from colorama import init, Fore, Back, Style

import sys 
import getopt

"""
Print the copyright for this tool
"""
def print_copyright():
    print(Fore.CYAN + Back.BLACK + "Automated client-side template injection (CSTI) detection for AngularJS!")
    print(Fore.CYAN + Back.BLACK + "Copyright (c) 2017 Tijme Gommers (see `LICENSE.md`).")
    print("")

"""
Print the options for this tool
"""
def print_usage():
    print("Usage: python angular.py <options>")
    print("")
    print("Options:")
    print("-u <uri>,      --uri=<uri>              Required        The hostname or URL to run the exploit on (e.g. https://www.example.ltd/).")
    print("-v,            --verify                 Optional        Extra check by a JavaScript engine to ensure the payload is executed.")
    #print("-c,            --crawl                  Optional        Crawl & test all available URL's on the hostname of the given URL.")
    #print("-q,            --quit-if-vulnerable     Optional        Stop testing if a vulnerable URL was found.")
    print("-h,            --help                   Optional        Print this help message.")
    print("")

"""
Get CLI arguments
"""
def parse_options(argv):
    input_uri = None
    input_help = False
    input_verify_exploit = False
    input_use_url_crawler = False
    input_quit_if_vulnerable = False
    
    try:                                
        opts, args = getopt.getopt(argv, "u:hvcq", ["uri=", "help", "verify", "crawl", "quit-if-vulnerable"])

        for opt, arg in opts:
            if opt in ("-u", "--uri"):
                input_uri = arg
            elif opt in ("-h", "--help"):
                input_help = True
            elif opt in ("-v", "--verify"):
                input_verify_exploit = True
            elif opt in ("-c", "--crawl"):
                input_use_url_crawler = True
            elif opt in ("-q", "--quit-if-vulnerable"):
                input_quit_if_vulnerable = True

    except getopt.GetoptError as e:
        print_usage()
        print(Fore.RED + Back.BLACK + "Error: " + str(e))               
        sys.exit(2)    

    if input_uri is None or input_help is True:
        print_usage()
        if input_help is False:
            print(Fore.RED + Back.BLACK + "Error: URI argument is required, please use --uri= or -u")     
        sys.exit()

    return (input_uri, input_verify_exploit, input_use_url_crawler, input_quit_if_vulnerable)

"""
Run scanner
"""
def main(argv):
    # Get the CLI arguments
    (input_uri, input_verify_exploit, input_use_url_crawler, input_quit_if_vulnerable) = parse_options(argv)

    Logging.info("Started scan");

    # Get website details, like the AngularJS version
    website_details = Scraper.get_instance().get_details(input_uri);

    # Verify the website uses AngularJS
    if not website_details["uses_angular"]:
        print(Fore.RED + Back.BLACK + "This website does not use AngularJS.")
        sys.exit()

    Logging.info("Found AngularJS version " + website_details["angular_version"])

    # Get the URI's to check
    urls = [input_uri]
    vulnerable_urls = []

    # TODO: remove the False when enabling the crawler.
    if input_use_url_crawler and False:
        Logging.info("Started crawler...")
        urls = Crawler.get_instance().get_urls(input_uri)
        Logging.info("Finished crawling")
        Logging.info("Found {} URI(s)".format(len(urls)))

    Logging.info("Going to test {} URI(s)".format(len(urls)))

    # Test the exploit on every URI
    exploit = Exploit.get_instance()

    for index, url in enumerate(urls):
        Logging.info("Testing URI {}/{}: {}".format(index + 1, len(urls), url))

        result = exploit.is_vulnerable(url, website_details["angular_version"], input_verify_exploit)

        if result is not False:
            vulnerable_urls.append(result)

        # TODO: remove the False when enabling the crawler.
        if result is not False and input_quit_if_vulnerable and False:
            break

    # Log the results
    Logging.info("Found {} vulnerable URI(s)".format(len(vulnerable_urls)))

    for index, vulnerable_url in enumerate(vulnerable_urls):
        Logging.red("Vulnerable URI: {}".format(vulnerable_url))

"""
Start with main method
"""
if __name__ == "__main__":
    init(autoreset=True)
    print_copyright()
    main(sys.argv[1:])