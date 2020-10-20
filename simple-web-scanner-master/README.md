# Simple web scanner

This is simple web application fuzzing tool for scanning SQL injection and XSS vulnerabilities on the Internet. Although many commercial or open-source web scanning tools are available on the internet such as: [Acunetix](https://www.acunetix.com/), [arachni](http://www.arachni-scanner.com/)... However its sources are complicated for dummy web pentester. Thus, this tool provides:

- The simplest way to understanding how the automatic tool detects SQL injection and XSS.
- Design a simple crawler and use it for testing vulnerability.
- A fuzzing method on query value parameters in URL.


## Installation

This program uses python 3.x. `virtualenv` is recommended for testing purpose. To check your python environment, you can use the following commands:

```
$ python3 --version
Python 3.5.2

$ pip3 --version
pip 9.0.1 from /usr/local/lib/python3.5/dist-packages (python 3.5)
```

### Requirements packages:

This program uses BeautifulSoup for parsing HTML content. You can install it by command:
```
pip3 install bs4
```



## Usage:

So, you have to define `seed_url` and `engine` arguments for this program.

```
python3 scan_cli.py --seedurl http://example.com --engine xss
```


## Program structure

```
.
├── crawler.py      # Simple webcrawler
├── parser.py       # HTML parser
├── README.md       # You are here
├── scan_cli.py     # main program, but it is not important. It just parses command line arguments
├── scanner_core.py # core scanner. Read this script carefully
├── sqli_scanner.py # SQL injection which extented from core scanner
├── vectors         # attacker vectors directory
│   ├── sqli_vectors.txt
│   └── xss_vectors.txt
└── xss_scanner.py  # XSS which extented from core scanner
```

## Notes

If you want to know how crawler works. You can modify `seed_url` line 89 in file crawler and run `python3 crawler.py` to see what happened.
