import requests as r
import re
from bs4 import BeautifulSoup as bs

domain = 'http://www.worldometers.info/'
url = domain + 'world-population/population-by-country'

print(url)
data = r.get(url)
s = data.status_code
t = data.elapsed.total_seconds()
print(s, t)
soup = bs(data.content, 'html.parser')
#imgs = soup.find_all('img')
#print(len(imgs))
h1 = soup.find_all('h1')
tabs = soup.find_all('th')
headers = [t.text.replace('\n', '') for t in tabs]
#th = [t.replace("<th>", '') for t in tabs]
th = headers[1:4]
pops = []
for i, row in enumerate(soup.find_all('tr')):
    try:
        d1, d2, d3 = row.find_all('td')[1:4]
        d1 = d1.find('a').text
        d2 = d2.text
        d3 = d3.text
        pops.append([d1, d2, d3])
    except:
        print('Error parsing row {}'.format(i))

countries = []
for i in pops:
    countries.append(i[0])

pad = (len(max(countries, key=len)) + 1)

for i in pops:
    print(i[0].ljust(pad) + i[1].ljust(14) + i[2])
