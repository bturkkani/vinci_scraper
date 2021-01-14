#!/usr/bin/env python
# coding: utf-8
"""
Created on Tue Jan 5 10:01:49 2021

@author: bturkkani
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
emails = []
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}
domain = input("domain (type 'done' when done): ")
while domain != 'done':
    domain = domain.split()
    for d in domain:
        tlist = []
        url = 'https://www.skymem.info/srch?q=' + d
        resp = requests.get(url, headers = headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            for t in soup('td'):
                tlist.append(t.find('a'))
                tlist = list(filter(None, tlist))
                for tl in tlist: emails.append(tl.text)
        else:
            print('Error ' + str(resp.status_code) + ': page not found or smt look it up')
            break
        query1 = 'email+"%40' + d + '"'
        query2 = 'email+mail+"%40' + d + '"'
        queries = [query1, query1]
        for q in queries:
            page = 0
            while page <= 90:
                url = 'https://www.google.com/search?q={}&start={}'.format(q,page)
                resp = requests.get(url, headers=headers)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.content, "html.parser")
                    for g in soup.find_all('div', class_='g'):
                        rc = g.find('div', class_='rc')
                        IsZvec = rc.find('div', class_='IsZvec')
                        spans = IsZvec.find('span', class_='aCOpRe').text
                        spansplit = spans.split()
                        for s in spansplit:
                            if '@' + d in s:
                                s = s.replace('(','')
                                s = s.replace(')','')
                                s = s.replace(':','')
                                s = s.replace(';','')
                                s = s.replace(',','')
                                if s[-1] == '.': s = s[:-1]
                                if s[0] == '.': s = s[1:]
                                emails.append(s)
                    page = page + 10
                else:
                    if resp.status_code == 429: print('Google blocked you. Try again tomorrow.')
                    else: print('Error ' + str(resp.status_code) + ': page not found or smt look it up')
                    break
    domain = input("domain (type 'done' when done): ")
emails = list(set(emails))
df = pd.DataFrame(emails)
df.to_excel('emails.xlsx')
df.to_csv('emails.csv')
df