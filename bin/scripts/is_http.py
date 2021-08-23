import requests as r

url = 'http://surx'

x = r.get(url)
data = x.text
code = x.status_code
print(code)
