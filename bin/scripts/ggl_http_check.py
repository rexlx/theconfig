import pymongo
from pymongo import MongoClient
import time
import requests as r


client = MongoClient('192.168.1.68', 27017)
my_db = client.http_response
my_collection = my_db.google

def probe():
    sites = [ 'mail', 'docs', 'music', 'photos', 'drive']
    for site in sites:
        url = 'https://' + site + '.google.com'
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
            insert_id = my_collection.insert_one(entry)
        except r.exceptions.ConnectionError:
            r_time = 0
            the_time = time.time()
            entry = {"url": url, "time": the_time, "response": r_time}
            insert_id = my_collection.insert_one(entry)
    
while True:
    probe()
    time.sleep(5)
