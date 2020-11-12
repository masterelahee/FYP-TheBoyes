import http.client
import argparse
import socket 
import ssl
import sys
import re

from urllib.parse import urlparse

class SecurityHeaders():
    def __init__(self):
        pass

    def evaluate_warn(self, header, contents):
        """ Risk evaluation function.
        Set header warning flag (1/0) according to its contents.
        Args:
            header (str): HTTP header name in lower-case
            contents (str): Header contents (value)
        """
        warn = 1

        if header == 'x-frame-options':
            if contents.lower() in ['deny', 'sameorigin']:
                warn = 0
            else:
                warn = 1

        if header == 'strict-transport-security':
            warn = 0

        """ Evaluating the warn of CSP contents may be a bit more tricky.
            For now, just disable the warn if the header is defined
            """
        if header == 'content-security-policy':
            warn = 0

        """ Raise the warn flag, if cross domain requests are allowed from any 
            origin """
        if header == 'access-control-allow-origin':
            if contents == '*':
                warn = 1
            else:
                warn = 0
    
        if header.lower() == 'x-xss-protection':
            if contents.lower() in ['1', '1; mode=block']:
                warn = 0
            else:
                warn = 1

        if header == 'x-content-type-options':
            if contents.lower() == 'nosniff':
                warn = 0
            else:
                warn =1

        """ Enable warning if backend version information is disclosed """
        if header == 'x-powered-by' or header == 'server':
            if len(contents) > 1:
                warn = 1
            else: 
                warn = 0

        return {'defined': True, 'warn': warn, 'contents': contents}

    def test_https(self, url):
        parsed = urlparse(url)
        protocol = parsed[0]
        hostname = parsed[1]
        path = parsed[2]
        sslerror = False
            
        conn = http.client.HTTPSConnection(hostname, context = ssl.create_default_context() )
        try:
            conn.request('GET', '/')
            res = conn.getresponse()
        except socket.gaierror:
            return {'supported': False, 'certvalid': False}
        except ssl.CertificateError:
            return {'supported': True, 'certvalid': False}
        except:
            sslerror = True

        # if tls connection fails for unexcepted error, retry without verifying cert
        if sslerror:
            conn = http.client.HTTPSConnection(hostname, timeout=5, context = ssl._create_stdlib_context() )
            try:
                conn.request('GET', '/')
                res = conn.getresponse()
                return {'supported': True, 'certvalid': False}
            except:
                return {'supported': False, 'certvalid': False}

        return {'supported': True, 'certvalid': True}

    def test_http_to_https(self, url, follow_redirects = 5):
        parsed = urlparse(url)
        protocol = parsed[0]
        hostname = parsed[1]
        path = parsed[2]
        if not protocol:
            protocol = 'http' # default to http if protocl scheme not specified

        if protocol == 'https' and follow_redirects != 5:
            return True
        elif protocol == 'https' and follow_redirects == 5:
            protocol = 'http'

        if (protocol == 'http'):
            conn = http.client.HTTPConnection(hostname)
        try:
            conn.request('HEAD', path)
            res = conn.getresponse()
            headers = res.getheaders()
        except socket.gaierror:
            print('HTTP request failed')
            return False

        """ Follow redirect """
        if (res.status >= 300 and res.status < 400  and follow_redirects > 0):
            for header in headers:
                if (header[0].lower() == 'location'):
                    return self.test_http_to_https(header[1], follow_redirects - 1) 

        return False

    def check_headers(self, url, follow_redirects = 0):
        """ Make the HTTP request and check if any of the pre-defined
        headers exists.
        Args:
            url (str): Target URL in format: scheme://hostname/path/to/file
            follow_redirects (Optional[str]): How deep we follow the redirects, 
            value 0 disables redirects.
        """

        """ Default return array """
        retval = {

            'x-frame-options': {'defined': False, 'warn': 1, 'contents': '', 'discription': 'provide clickjacking protection that A malicious technique that tricks the user into clicking on something other than what they perceive to be clicking, potentially allowing an attacker to leak confidential information or gain control over their computer.  ' },
            'strict-transport-security': {'defined': False, 'warn': 1, 'contents': '', 'discription': 'is for HTTP Strict Transport Security In general, when HTTPS is forced, the server can convert it using 302 Redirect. However, this can act as a vulnerability point. It is recommended to induce HTTPS connection using 302 Redirect and force HTTPS to the client browser, which is HSTS (HTTP Strict Transport Security). Since it is forced by the client (browser), the connection itself using Plain Text (HTTP) is not attempted from the beginning and has the advantage that it is blocked on the client side. ' },
            'access-control-allow-origin': {'defined': False, 'warn': 0, 'contents': '', 'discription': 'specifies either a single origin, which tells browsers to allow that origin to access the resource' },
            'content-security-policy': {'defined': False, 'warn': 1, 'contents': '', 'discription': 'In order not to load unwanted files(eg. xss), this header allows  specified external sources only.' },
            'x-xss-protection': {'defined': False, 'warn': 1, 'contents': '', 'discription': ' is designed to enable the cross-site scripting (XSS) filter built into modern web browsers.' }, 
            'x-content-type-options': {'defined': False, 'warn': 1, 'contents': '', 'discription': 'response HTTP header is a marker used by the server to indicate that the MIME types advertised in the Content-Type headers should not be changed and be followed.' },
            'x-powered-by': {'defined': False, 'warn': 0, 'contents': '' },
            'server': {'defined': False, 'warn': 0, 'contents': '' }

        }

        parsed = urlparse(url)
        protocol = parsed[0]
        hostname = parsed[1]
        path = parsed[2]
        if (protocol == 'http'):
            conn = http.client.HTTPConnection(hostname)
        elif (protocol == 'https'):
                # on error, retry without verifying cert
                # in this context, we're not really interested in cert validity
                ctx = ssl._create_stdlib_context()
                conn = http.client.HTTPSConnection(hostname, context = ctx )
        else:
            """ Unknown protocol scheme """
            return {}
    
        try:
            conn.request('HEAD', path)
            res = conn.getresponse()
            headers = res.getheaders()
            
        except socket.gaierror:
            print('HTTP request failed')
            return False

        """ Follow redirect """
        if (res.status >= 300 and res.status < 400  and follow_redirects > 0):
            for header in headers:
                if (header[0].lower() == 'location'):
                    redirect_url = header[1]
                    if not re.match('^https?://', redirect_url):
                        redirect_url = protocol + '://' + hostname + redirect_url
                    return self.check_headers(redirect_url, follow_redirects - 1) 
                
        """ Loop through headers and evaluate the risk """
        for header in headers:

            #set to lowercase before the check
            headerAct = header[0].lower()

            if (headerAct in retval):
                retval[headerAct] = self.evaluate_warn(headerAct, header[1])

        return retval

if __name__ == "__main__":


    url = 'unpatchedfyp.hopto.org'

    foo = SecurityHeaders()

    parsed = urlparse(url)
    if not parsed.scheme:
        url = 'http://' + url # default to http if scheme not provided



    headers = foo.check_headers(url)

    if not headers:
        print ("Failed to fetch headers, exiting...")
        sys.exit(1)


    ###json output

    print('{\n\t"name": "security header",\n\t"headers": [')
    for header, value in headers.items():
        if value['warn'] == 1:
            if value['defined'] == False:
                print('\t{\n\t\t"name": " '+ header + '",\n\t\t"discription": "' + value['discription'] + '"\n\t},')
            else:
                print('\t{\n\t\t"name": " Header \'' + header + '\' contains value \'' + value['contents'] + '",\n\t\t"discription": "Hackers can use this information to find out vulnerabilities easily in the server. For security purposes, it is necessary to use this header to prevent the transmission of information."\n\t},')

    https = foo.test_https(url)
    if not https['supported']:
        print('\t{\n\t\t"name": "HTTPS supported FAIL",\n\t\t"discription": "HTTPS protects the communication between your browser and server from being intercepted and tampered with by attackers. This provides confidentiality, integrity and authentication to the vast majority of today\'s WWW traffic. "\n\t},')

    if not https['certvalid']:
        print('\t{\n\t\t"name": "HTTPS valid certificate FAIL",\n\t\t"discription": "a HTTPS connection relies on an SSL certificate in order for the procedure to become secure. The reason for this is because the SSL certificate is responsible for \'encrypting\' online data, specifically between the visitor\'s browser and the server. "\n\t},')

    if not foo.test_http_to_https(url, 5):
        print('\t{\n\t\t"name": "HTTP -> HTTPS redirect FAIL",\n\t\t"discription": "if you do allow HTTP and redirect to HTTPS, that cookies are marked as secure. "\n\t},')

    print('\t]\n}')

