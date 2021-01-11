#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from bs4 import BeautifulSoup

results = []
domain = input("domain (omit @) (type 'done' when done): ")
while domain != 'done':
    tlist = []
    url = 'https://www.skymem.info/srch?q=' + domain
    u_a = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/84.0"
    headers = {"user-agent": u_a}
    resp = requests.get(url, headers = headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        for t in soup('td'):
            tlist.append(t.find('a'))
            tlist = list(filter(None, tlist))
            for tl in tlist:
                results.append(tl.text)
    else:
        print('Error ' + str(resp.status_code) + ': page not found or smt dunno')
        break
    query1 = 'email+"%40' + domain + '"'
    query2 = 'email+mail+"%40' + domain + '"'
    queries = [query1, query1]
    for q in queries:
        page = 0
        while page <= 90:
            url = 'https://www.google.com/search?q={}&start={}'.format(q,page)
            u_a = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/84.0"
            headers = {"user-agent": u_a}
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, "html.parser")
                for g in soup.find_all('div', class_='g'):
                        rc = g.find('div', class_='rc')
                        IsZvec = rc.find('div', class_='IsZvec')
                        spans = IsZvec.find('span', class_='aCOpRe').text
                        spansplit = spans.split()
                        for s in spansplit:
                            if '@' + domain in s:
                                s = s.replace('(','')
                                s = s.replace(')','')
                                s = s.replace(':','')
                                s = s.replace(';','')
                                s = s.replace(',','')
                                results.append(s)
                page = page+10
            else:
                print('Error ' + str(resp.status_code) + ': page not found or smt dunno')
                break
    domain = input("domain (omit @) (type 'done' when done): ")
results = list(set(results))
df = pd.DataFrame(results)
df.to_excel('results.xlsx')
df.to_csv('results.csv')