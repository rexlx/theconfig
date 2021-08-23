import requests as r
#from requests.auth import HTTPBasicAuth

manifest = ['drive', 'photos', 'music', 'mail']
for i in manifest:
    url = "https://" + i + ".google.com"
    data = r.get(url)
    code = int(data.status_code)
    latency = data.elapsed.total_seconds()
    if code == 200:
        print(i + ": " + str(code) + "  " + str(latency))
    else:
        print(i + ": " + str(code) + "  " + str(latency) + " ERROR")

print('\n')
