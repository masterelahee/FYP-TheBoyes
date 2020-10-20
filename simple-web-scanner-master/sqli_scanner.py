from scanner_core import ScannerCore


class SqliScanner(ScannerCore):

    def __init__(self):
        ScannerCore.__init__(self)
        self.SIGNATURE = ['SQL syntax', 'MySQL server', 'mysql_num_row']
        self.load_vectors('./vectors/sqli_vectors.txt')

    def find_signature(self, html_content):
        # return True if it finds signature in html content.
        # We don't need to parse html content since SQLi vulnerabily don't need to validate html semantic.
        if any(sig in html_content for sig in self.SIGNATURE):
            return True
        else:
            return False

    def replacement_param(self, param_value, vector):
        return param_value[0] + vector


