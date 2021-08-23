import time, uuid
import requests as r

proxy = "http://surx:8080/api/http/"
start = time.time()
my_time = 0
c, c400 , c201 = 0, 0, 0
attempts = 0
while my_time <= 200:
    myid = uuid.uuid4().hex
    now = time.time()
    my_time = now - start
    url = myid
    the_time = my_time
    r_time = 999999999999999999
    entry = {"url": url, "time": the_time, "response": r_time}
    attempts += 1
    confirmation = r.post(proxy, entry)
    code = confirmation.status_code
    ntime = confirmation.elapsed.total_seconds()
    data = confirmation.text
    c += 1
    if code != 201:
        c400 += 1
    else:
        c201 += 1
    #print(code, ntime)
    #print(data)
    time.sleep(0.001)

end = time.time() - start
print(end, attempts, c)
print(c201, c400)
input("ok")
