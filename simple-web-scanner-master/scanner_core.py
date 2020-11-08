from urllib.parse import urlparse, parse_qs, urlunparse, urlencode, unquote
import urllib.request


class ScannerCore(object):
    """docstring for ScannerCore"""

    def __init__(self):
        # define vectors list
        self.vectors = list()
        self.SIGNATURE = None

    def load_vectors(self, file):
        with open(file) as f:
            for line in f:
                self.vectors.append(line.strip())

    def find_signature(self):
        # This method will be overwrited in subclass
        raise NotImplemented

    def replacement_param(self, value, vector):
        # This method will be overwrited in subclass
        raise NotImplemented

    def build_malicious_url(self, url):
        # The query is: first=1&second=2
        # key is first and value is 1.
        # So, first=1&second=2 becomes {first: 1, second: 2}
        #
        # As I explained in document. We have to replace value in query string to determine vulnerabilites.
        # the following steps replace value in query to test vulnerablity

        # we have to parse url to get query string
        parsed = urlparse(url)
        query_dict = parse_qs(parsed.query)


        # for each key, value in query dict. we are going replace value with attack vectors
        for key, value in query_dict.items():
            # replace value with attack vector
            # if SIGNATURE = '9x9x9x9x9x9', value becomes
            # <script>alert("9x9x9x9x9x9")</script>

            for vector in self.vectors:
                new_value = self.replacement_param(value, vector)

                # Create new query
                # we can use the trick urlencode to convert a dict {key:value} to key=value
                # `urlencode` encodes query to
                #
                tmp_dict = query_dict.copy()
                tmp_dict[key] = new_value
                new_query = unquote(urlencode(tmp_dict, doseq=True))
                del tmp_dict


                # combine query and URL to make malicious url
                malicious_url = urlunparse(parsed._replace(query=new_query))


                # uncomment the following line to print maclious url
                # print(malicious_url)
                yield malicious_url

    def analyze(self, url):
        # This function will get requests each vulnerable url to server to get response
        for mal_url in self.build_malicious_url(url):

            try:
                res = urllib.request.urlopen(mal_url)
            except HTTPError as e: # http status is not 200, continue next malcious url
                print(url, e)
                continue

            html_content = res.read().decode("utf-8", 'ignore') # decode HTML content in UTF-8

            if self.find_signature(html_content):
                yield mal_url

    def scan(self, url):
        # return all exploit url
        for mal_url in self.analyze(url):
            yield mal_url
