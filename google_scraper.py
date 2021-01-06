#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from bs4 import BeautifulSoup

results = []
url = input("url (type 'done' when done): ")
while url != 'done':
    u_a = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": u_a}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        for g in soup.find_all('div', class_='g'):
            rc = g.find('div', class_='rc')
            s = g.find('div', class_='s')
            if rc:
                divs = rc.find_all('div', recursive=False)
                if len(divs) >= 2:
                    anchor = divs[0].find('a')
                    link = anchor['href']
                    title = anchor.find('h3').text
                    item = {"title": title, "link": link}
                    results.append(item)
    url = input("url (type 'done' when done): ")
df = pd.DataFrame(results)
df.drop_duplicates()
#output both csv and excel
df.to_excel('output/results.xlsx')
df.to_csv('output/results.csv', header=True)
