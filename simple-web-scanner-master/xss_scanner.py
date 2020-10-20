from scanner_core import ScannerCore
from jason import j


class XssScanner(ScannerCore):

    def __init__(self):
        ScannerCore.__init__(self)
        self.SIGNATURE = 'XSS'
        self.load_vectors('./vectors/xss_vectors.txt')

    def replacement_param(self, param_value, vector):
        # __SIGNATURE__ is place holder in attack vectors
        # replace with signatures
        v = vector.replace('__SIGNATURE__', self.SIGNATURE)
        return v

    def find_signature(self, html_content):
        # return True if it finds signature in script content else False
        # we have to parse HTML since script only works if HTML is correct syntax.
        parser = j(html_content)
        if any(self.SIGNATURE in s for s in parser.script_text):
            return True
        else:
            return False


