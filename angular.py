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

from classes.Exploit import Exploit

import sys 
import getopt

"""
Print some documentation for this exploit
"""
def usage():
    print('Automated client-side template injection detection for AngularJS')
    print('')
    print('Usage: angular <options>')
    print('')
    print('Options:')
    print('-u <host_url>,   --url=<host_url>       The website to run the exploit on (e.g. https://www.example.ltd).')
    print('-j,              --javascript-engine    Extra check by a JavaScript engine to ensure the payload is executed.')
    print('-h,              --help                 Print this help message.')
    print('')

"""
Get CLI arguments
"""
def parse_options(argv):
    input_url = None
    use_javascript_engine = False
    
    try:                                
        opts, args = getopt.getopt(argv, 'u:jh', ['url=', 'javascript-engine', 'help'])

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit()
            elif opt in ('-j', '--javascript-engine'):
                use_javascript_engine = True
            elif opt in ('-u', '--url'):
                input_url = arg

        return (input_url, use_javascript_engine)

    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)    

"""
Run scanner
"""
def main(argv):
    (input_url, use_javascript_engine) = parse_options(argv)

    # TODO: Automatically check this based on the input_url
    input_version = '1.5.5';

    # TODO: Get all URLS on the website that contain query parameters

    # TODO: Iterate over all those results and run the exploit
    exploit = Exploit.get_instance()
    result = exploit.is_vulnerable(input_url, input_version, use_javascript_engine)

    print("Website is vulnerable: \n" + str(result))

"""
Start with main method
"""
if __name__ == "__main__":
    main(sys.argv[1:])