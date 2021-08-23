import time
import requests as r

def probe():
    sites = ["https://www.wikipedia.org", 
             "https://www.forums.fedoraforum.org",
             "https://github.com"]
    for site in sites:
        url = site
        try:
            data = r.get(url)
            stat = int(data.status_code)
            time_spent = data.elapsed.total_seconds()
            if stat == 200:
                r_time = time_spent
            else:
                r_time = 0
            the_time = time.time()
            entry = {"url": url, "time": the_time, "response": r_time}
            proxy = "http://surx:8080/api/http/"
            confirmation = r.post(proxy, entry)
            #print(confirmation.status_code)
        except r.exceptions.ConnectionError:
            r_time = 0
            the_time = time.time()
            entry = {"url": url, "time": the_time, "response": r_time}
            proxy = "http://surx:8080/api/http/"
            confirmation = r.post(proxy, entry)

while True:
    probe()
    time.sleep(.10)
