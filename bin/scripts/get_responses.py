import pymongo
from pymongo import MongoClient
import os, time


#db_dump_file = '/home/rxlx/bin/data/nfm_db.dump'

start = time.time()
#client = MongoClient('localhost', 27017)
client = MongoClient('192.168.1.68', 27017)
my_db = client.http_response
#my_col = my_db.nfm

sites = ["https://www.wikipedia.org",
             "https://www.forums.fedoraforum.org",
             "https://github.com"]
for site in sites:
    if 'www' in site:
       db_dump_file = site[11:] + '.dump'
    else:
        db_dump_file = site[7:] + '.dump'
    url = site
    x = my_db.responses.find(
        {"url": url},
        {"response": 1, "time": 1, "_id": 0})
    try:
        os.remove(db_dump_file)
    except OSError:
        pass
    with open(db_dump_file, 'a') as f:
        for entry in x:
            f.write(str(entry) + '\n')

total_entries = my_db.responses.count()

down_time = my_db.responses.find( {'response': 0 }, {'_id': 0} )
#for i in down_time:
#    print(i)

print('total entries: ' + str(total_entries))
now = time.time()
length = now - start
print("\ntook " + str(length))
