#!/usr/bin/env python
# coding: utf-8
"""
Created on Tue Dec 29 14:05:26 2020

@author: bturkkani
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

links = []
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/84.0"}
key = input("key phrase (type 'done' when done): ")
pdat = input("pages to scrape (type 'std' after number if constant e.g '1 std'): ")
while key != 'done':
    pdat.split()
    pmax = (int(pdat.split()[0])-1)*10
    page = 0
    while page <= pmax:
        key = key.replace(' ', '+')
        url = 'https://www.google.com/search?q={}&start={}'.format(key,page)
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            for g in soup.find_all('div', class_='g'):
                    rc = g.find('div', class_='rc')
                    if rc:
                        divs = rc.find_all('div', recursive=False)
                        if len(divs) >= 2:
                            anchor = divs[0].find('a')
                            link = anchor['href']
                            title = anchor.find('h3').text
                            item = {"title": title,"link": link}
                            links.append(item)
            page = page + 10
        else:
            if resp.status_code == 429: print('Google blocked you. Try again tomorrow.')
            else: print('Error ' + str(resp.status_code) + ': page not found or smt look it up')
            break
    key = input("key phrase (type 'done' when done): ")
    if key != 'done':
        if pdat.split()[-1] != 'std':
            pdat = input("pages to scrape (type 'std' after number if constant e.g '1 std'): ")
df = pd.DataFrame(links)
df.drop_duplicates()
df.to_excel('links.xlsx')
df.to_csv('links.csv')
df