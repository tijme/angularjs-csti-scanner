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

from acstis.Driver import Driver
from acstis.Logging import Logging
from colorama import init, Fore, Back, Style

import sys 
import getopt

def print_copyright():
    print(Fore.CYAN + Back.BLACK + "AngularJS CSTI Scanner (ACSTIS)")
    print(Fore.CYAN + Back.BLACK + "Copyright (c) 2017 Tijme Gommers (see `LICENSE.md`).")
    print("")

def print_usage():
    print("Usage: acstis <options>")
    print("")
    print("Options:")
    print("-u <uri>,      --uri=<uri>              Required        The hostname or URL to run the exploit on (e.g. https://www.example.ltd/).")
    print("-v,            --verify                 Optional        Extra check by a JavaScript engine to ensure the payload is executed.")
    print("-c,            --crawl                  Optional        Crawl & test all available URL's on the hostname of the given URL.")
    print("-q,            --quit-if-vulnerable     Optional        Stop testing if a vulnerable URL was found.")
    print("-h,            --help                   Optional        Print this help message.")
    print("")

def parse_options(argv):
    input_uri = None
    input_help = False
    input_verify_exploit = False
    input_use_crawler = False
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
                input_use_crawler = True
            elif opt in ("-q", "--quit-if-vulnerable"):
                input_quit_if_vulnerable = True

    except getopt.GetoptError as e:
        print_usage()
        print(Fore.RED + Back.BLACK + "Error: " + str(e))
        sys.exit(1)    

    if input_uri is None or input_help is True:
        print_usage()
        if input_help is False:
            print(Fore.RED + Back.BLACK + "Error: URI argument is required, please use --uri= or -u")     
        sys.exit(1)

    return (input_uri, input_verify_exploit, input_use_crawler, input_quit_if_vulnerable)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
        
    init(autoreset=True)
    print_copyright()
    
    (uri, verify_exploit, use_crawler, quit_if_vulnerable) = parse_options(argv)
    Driver(uri, verify_exploit, use_crawler, quit_if_vulnerable)

if __name__ == "__main__" or __name__ == "acstis_scripts.acstis_cli":
    main(sys.argv[1:])