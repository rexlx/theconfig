import requests as r

url = 'https://ipleak.net/json'

data = r.get(url)
time = data.elapsed.total_seconds()
s_code = data.status_code
txt = data.json()

print(time, s_code)
print(txt)

