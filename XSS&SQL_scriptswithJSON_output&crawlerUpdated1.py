import mechanize
import http.cookiejar as cookielib
from bs4 import BeautifulSoup
import html2text
import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
s = requests.Session()
br = mechanize.Browser()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    # get the form action (target url)
    action = form.attrs.get("action").lower()
    # get the form method (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()
    # get all the input details such as type and name
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, value):
    # construct the full URL (if the url provided in action is relative)
    target_url = urljoin(url, form_details["action"])
    # get the inputs
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        # replace all text and search values with `value`
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            # if input name and value are not None, 
            # then add them to the data of form submission
            data[input_name] = input_value
        
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        # GET request
        return requests.get(target_url, params=data)

def scan_xss(url):
    # get all the forms from the URL
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    js_script = "<script>alert('hi')</script>"
    # returning value
    is_vulnerable = False
    # iterate over all forms
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            print(f"[+] XSS Detected on {url}")
            print(f"[*] Form details:")
            
            form_inputs = [{list(form_details)[2]:form_details["inputs"]}]
            print(form_inputs)
            with open('data.json','a+') as outfile:
                json.dump(form_inputs,outfile)
            is_vulnerable = True
            # won't break because we want to print available vulnerable forms
    return is_vulnerable
def is_vulnerable(response):
    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
    }
    for error in errors:
        # if you find one of these errors, return True
        if error in response.content.decode().lower():
            return True
    # no error detected
    return False

def scan_sql_injection(url):
    # test on URL
    for c in "\"'":
        # add quote/double quote character to the URL
        new_url = f"{url}{c}"
        print("[!] Trying", new_url)
        # make the HTTP request
        res = s.get(new_url)
        if is_vulnerable(res):
            # SQL Injection detected on the URL itself, 
            # no need to preceed for extracting forms and submitting them
            print("[+] SQL Injection vulnerability detected, link:", new_url)
            return
    # test on HTML forms
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            # the data body we want to submit
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    # any input form that is hidden or has some value,
                    # just use it in the form body
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    # all others except submit, use some junk data with special character
                    data[input_tag["name"]] = f"test{c}"
                elif input_tag["type"]  == "submit":
                    input_tag["Issue"] = "SQL Injection"
                    input_tag["Description"] = "SQL Injection allows attacker to modify/delete database related values"
                    input_tag["Remedy"] = "Input Sanitization, Escaping User Suppllied Inputs, Parameterized Queries etc"
                    input_tag["Useful Links"] = "https://portswigger.net/web-security/sql-injection, https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"
            # join the url with the action (form request URL)
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(url, data=data)
            elif form_details["method"] == "get":
                res = s.get(url, params=data)
            # test whether the resulting page is vulnerable
            if is_vulnerable(res):
                print("[+] SQL Injection vulnerability detected, link:", url)
                print("[+] Form:")
                print(form_details)
                break
def trying(url_org):
    
    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    br.addheaders = [('User-agent', 'Chrome')]

    # The site we will navigate into, handling it's session
    br.open(url_org)

	

    getpage= requests.get(url_org)

    getpage_soup= BeautifulSoup(getpage.text, 'html.parser')

    all_links= getpage_soup.findAll('a')
    print("\n")
    for link in all_links:
        if "http" not in link.attrs['href']:
            print(url_org+'/'+link.attrs['href'])
            url = url_org+'/'+link.attrs['href']
            print(scan_xss(url))
                

if __name__ == "__main__":
    print("XSS Vulnerability")
    print("XSS Vulnerabilty allows attacker to mess with an application by posing as victim use and access user data.")
    print("Filtering of inputs, type casting, JavaScript Unicode Escapes etc")
    print("https://portswigger.net/web-security/cross-site-scripting,https://owasp.org/www-community/attacks/xss/#")
    url = "http://html5.vulnweb.com/"
    url_sql = "http://testphp.vulnweb.com/login.php"
    
    #scan_sql_injection(url_sql)
    trying(url)
    
    
    



    
