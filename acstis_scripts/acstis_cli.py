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

import argparse
import colorlog
import logging

from nyawc.Options import Options
from acstis.Driver import Driver
from acstis.helpers.PackageHelper import PackageHelper

def require_arguments():
    """Get the arguments from CLI input.

    Returns:
        :class:`argparse.Namespace`: A namespace with all the parsed CLI arguments.

    """

    parser = argparse.ArgumentParser(
        prog=PackageHelper.get_alias(),
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=150, width=150)
    )

    optional = parser._action_groups.pop()
    required = parser.add_argument_group("required arguments")

    required.add_argument("-d", "--domain", help="the domain to scan (e.g. finnwea.com)", required=True)

    optional.add_argument("-pmm", "--protocol-must-match", help="only scan pages with the same protocol as the startpoint (e.g. only https)", action="store_true")
    optional.add_argument("-sos", "--scan-other-subdomains", help="also scan pages that have another subdomain than the startpoint", action="store_true")
    optional.add_argument("-soh", "--scan-other-hostnames", help="also scan pages that have another hostname than the startpoint", action="store_true")
    optional.add_argument("-sot", "--scan-other-tlds", help="also scan pages that have another tld than the startpoint", action="store_true")
    optional.add_argument("-siv", "--stop-if-vulnerable", help="stop scanning if a vulnerability was found", action="store_true")
    optional.add_argument("-md", "--max-depth", help="the maximum search depth (default is unlimited)", type=int)
    optional.add_argument("-mt", "--max-threads", help="the maximum amount of simultaneous threads to use (default is 8)", type=int, default=8)

    parser._action_groups.append(optional)
    return parser.parse_args()

def setup_logger():
    """Setup ColorLog to enable colored logging output."""

    # Colored logging
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s[%(levelname)s] %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "white",
            "SUCCESS": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white"
        }
    ))

    logger = colorlog.getLogger()
    logger.addHandler(handler)

    # Also show INFO logs
    logger.setLevel(logging.INFO)

    # Add SUCCESS logging
    logging.SUCCESS = 25
    logging.addLevelName(
        logging.SUCCESS,
        "SUCCESS"
    )

    # Disable Selenium logging
    selenium_logger = logging.getLogger("selenium.webdriver.remote.remote_connection")
    selenium_logger.setLevel(logging.WARNING)

    setattr(
        logger,
        "success",
        lambda message, *args: logger._log(logging.SUCCESS, message, args)
    )

def print_banner():
    """Print a useless ASCII art banner to make things look a bit nicer."""

    print("""
 █████╗  ██████╗███████╗████████╗██╗███████╗
██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║██╔════╝
███████║██║     ███████╗   ██║   ██║███████╗
██╔══██║██║     ╚════██║   ██║   ██║╚════██║
██║  ██║╚██████╗███████║   ██║   ██║███████║
╚═╝  ╚═╝ ╚═════╝╚══════╝   ╚═╝   ╚═╝╚══════╝
Version """ + PackageHelper.get_version() + """ - Copyright 2017 Tijme Gommers <tijme@finnwea.com>
    """)

def main():
    """Start the scanner."""

    print_banner()
    setup_logger()

    args = require_arguments()

    options = Options()

    options.scope.protocol_must_match = args.protocol_must_match
    options.scope.subdomain_must_match = not args.scan_other_subdomains
    options.scope.hostname_must_match = not args.scan_other_hostnames
    options.scope.tld_must_match = not args.scan_other_tlds
    options.scope.max_depth = args.max_depth
    options.performance.max_threads = args.max_threads

    driver = Driver(args, options)
    driver.start()

if __name__ == "__main__":
    main()
