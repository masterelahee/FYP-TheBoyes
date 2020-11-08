from jason import j
from urllib.parse import urlparse

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin


class Crawler(object):

    def __init__(self, seedurl):
        self.seedurl = seedurl
        self.urlseen = set()  # store URLs

        # parse seed url to get domain.
        # crawler does not support external domain.
        urlparsed = urlparse(seedurl)
        self.domain = urlparsed.netloc

    def get_links(self, html):
        """
        Parse return link in html contents
        by finding href attribute in a tag.
        """

        hrefs = set()
        parser = j(html)

        # get href tags from parsed results
        for href in parser.hrefs:
            u_parse = urlparse(href)

            # check whether href content is same domain with seed url
            if u_parse.netloc == '' or u_parse.netloc == self.domain:
                hrefs.add(href)
        return hrefs

    def fetch(self, url):
        """
        return fetch HTML content from url
        return empty string if response raise an HTTPError (not found, 500...)
        """

        try:
            req = Request(url)
            res = urlopen(req)
            return res.read().decode('utf-8', 'ignore')

        except HTTPError as e:
            print('ERROR: %s \t  %s' % (url, e.code))
            return ''
        except URLError as e:
            print('Reason: ', e.reason)
            return ''

    def crawl(self):
        # add seed url to url frontier
        # URL frontier is the list which stores found URL but not yet crawled.
        # it works like a queue.
        url_frontier = list()
        url_frontier.append(self.seedurl)

        while url_frontier:
            url = url_frontier.pop()  # get url from frontier

            # do not crawl twice the same page
            if url not in self.urlseen:
                html = self.fetch(url)

                if html:  # if reponse has html content
                    print('Crawl: ', url)
                    self.urlseen.add(url)

                for href in self.get_links(html):
                    # join seed url and href, to get url
                    joinlink = urljoin(self.seedurl, href)
                    # print("joing href >> ", joinlink)  # uncomment this line to understand
                    url_frontier.append(joinlink)

    @property
    def crawled_urls(self):
        self.crawl()
        return self.urlseen


if __name__ == '__main__':

    seedurl = "http://203.249.90.9:5000/"
    crawler = Crawler(seedurl)
    # crawler.crawl()
    for url in crawler.crawled_urls:
        print('>>>', url)
