#!/usr/bin/python3

import sys
from crawler import Crawler
from sqli_scanner import SqliScanner
from xss_scanner import XssScanner

from urllib.parse import urlparse
import argparse

url="https://swinburne.edu.my"
seedurl="https://swinburne.edu.my"
def valid_url(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        return False
    if not parsed.netloc:
        return False
    else:
        return True


def work(seedurl, scanner):
    scan_results = set()
    crawler = Crawler(seedurl)
    for url in crawler.crawled_urls:
        for mal in scanner.scan(url):
            if mal not in scan_results:
                # print(mal)
                scan_results.add(mal)


    print("\n !! REPORT !! ")
    for malurl in scan_results:
        print(malurl)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(prog='Simple Web scanner')
    # parser.add_argument('--seedurl', help='seed url', required=True)
    # parser.add_argument('--engine', help='Type of engine \"sqli\" or \"xss\". Default engine is XSS')
    # args = parser.parse_args()

    # get seed url
    # seedurl = args.seedurl

    # get from aguments. set default 'xss'
    engine = 'xss'

    if not valid_url(seedurl):
        print("seedurl should follow RFC 3986. For example: http://domain.com/")
        sys.exit(1)

    # set up engine

    if engine == 'xss':
        scanner = XssScanner()
    elif engine == 'sqli':
        scanner = SqliScanner()
    else:
        parser.print_help()
        sys.exit(1)

    print("SELECTED %s engine" % engine)

    # everything is fine
    work(seedurl, scanner)
