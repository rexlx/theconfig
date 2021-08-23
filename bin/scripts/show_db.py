import pymongo
from pymongo import MongoClient
import os


db_dump_file = '/home/rxlx/bin/data/ok.dump'

#client = MongoClient('localhost', 27017)
client = MongoClient('127.0.0.1', 27017)
my_db = client.http_response
#my_col = my_db.nfm

sites = ['mail', 'docs', 'music', 'photos', 'drive']
for site in sites:
    db_dump_file = '/home/rxlx/bin/data/' + site + '.dump'
    url = 'https://' + site + '.google.com'
    x = my_db.google.find(
        {"url": url},
        {"response": 1, "time": 1, "_id": 0})
    try:
        os.remove(db_dump_file)
    except OSError:
        pass
    with open(db_dump_file, 'a') as f:
        for entry in x:
            f.write(str(entry) + '\n')

total_entries = my_db.google.count()

#down_time = my_db.google.find( {'response': 0 }, {'_id': 0} )
#for i in down_time:
#    print(i)

print('total entries: ' + str(total_entries))
