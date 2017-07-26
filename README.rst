.. raw:: html

   <p align="center">

.. image:: https://rawgit.com/tijme/angularjs-csti-scanner/refactor/.github/logo.svg?pypi=png.from.svg
   :width: 300px
   :height: 300px
   :alt: AngularJS Client-Side Template Injection Logo

.. raw:: html

   <br class="title">

.. image:: https://img.shields.io/pypi/v/acstis.svg
   :target: https://pypi.python.org/pypi/acstis/
   :alt: PyPi version

.. image:: https://img.shields.io/pypi/pyversions/acstis.svg
   :target: https://www.python.org/
   :alt: Python version

.. image:: https://img.shields.io/pypi/l/acstis.svg
   :target: https://github.com/tijme/acstis/blob/master/LICENSE.rst
   :alt: License: MIT

.. raw:: html

   </p>
   <h1>Angular Client-Side Template Injection Scanner</h1>

ACSTIS helps you to scan certain web applications for AngularJS Client-Side Template Injection (sometimes referred to as CSTI, sandbox escape or sandbox bypass). It supports scanning a single request but also crawling the entire web application for the AngularJS CSTI vulnerability.

Table of contents
-----------------

-  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `Issues <#issues>`__
-  `License <#license>`__

Installation
------------

First make sure you're on `Python 2.7/3.3 <https://www.python.org/>`__ or higher. Then run the command below to install ACSTIS.

``$ pip install --upgrade acstis``

Usage
-----

**Scan a single URL**

``acstis -d https://finnwea.com/some/page/?category=23``

**Scan a single URL (and verify that the alert pops)**

``acstis -vp -d https://finnwea.com/some/page/?category=23``

**Scan an entire domain**

``acstis -c -d https://finnwea.com/``

**Scan an entire domain (and stop if a vulnerability was found)**

``acstis -c -siv -d https://finnwea.com/``

**All command line options**

.. code:: text

   usage: acstis [-h] -d DOMAIN [-c] [-vp] [-av ANGULAR_VERSION] [-pmm] [-sos] [-soh] [-sot] [-siv] [-md MAX_DEPTH] [-mt MAX_THREADS]

   required arguments:
       -d DOMAIN, --domain DOMAIN                              the domain to scan (e.g. finnwea.com)

   optional arguments:
       -h, --help                                              show this help message and exit
       -c, --crawl                                             use the crawler to scan all the entire domain
       -vp, --verify-payload                                   use a javascript engine to verify if the payload was executed (otherwise false positives may occur)
       -av ANGULAR_VERSION, --angular-version ANGULAR_VERSION  manually pass the angular version (e.g. 1.4.2) if the automatic check doesn't work
       -pmm, --protocol-must-match                             (crawler option) only scan pages with the same protocol as the startpoint (e.g. only https)
       -sos, --scan-other-subdomains                           (crawler option) also scan pages that have another subdomain than the startpoint
       -soh, --scan-other-hostnames                            (crawler option) also scan pages that have another hostname than the startpoint
       -sot, --scan-other-tlds                                 (crawler option) also scan pages that have another tld than the startpoint
       -siv, --stop-if-vulnerable                              (crawler option) stop scanning if a vulnerability was found
       -md MAX_DEPTH, --max-depth MAX_DEPTH                    (crawler option) the maximum search depth (default is unlimited)
       -mt MAX_THREADS, --max-threads MAX_THREADS              (crawler option) the maximum amount of simultaneous threads to use (default is 8)

**Authentication, Proxies, Cookies, Headers & Scope options**

These options are not implemented in the command line interface of ACSTIS. Please use the scripts in the `examples <https://github.com/tijme/angularjs-csti-scanner/tree/master/examples>`_ folder to implement them.

Issues
------

Issues or new features can be reported via the GitHub issue tracker. Please make sure your issue or feature has not yet been reported by anyone else before submitting a new one.

License
-------

ACSTIS is open-sourced software licensed under the `MIT license <https://github.com/tijme/angularjs-csti-scanner/blob/master/LICENSE.rst>`__.
