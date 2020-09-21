# midiscraper.py
#Zoe, 2020

from bs4 import BeautifulSoup
import requests
import re 
import os
import sys

if (len(sys.argv) == 1):
    midi = input("Enter the musecore url for the midi you want to download: ")
    r = requests.get(midi.rstrip())
elif (len(sys.argv) == 2) :
    r = requests.get(sys.argv[-1])

soup = BeautifulSoup(r.text, 'html.parser')
page = str(soup)

q = re.search(r'(http|https):\/\/([\w]*)\.(([\w]*)\/){5}(([0-9]*)\/){4}([\w]*)\/(score)', page)

url = q.group(0) + '.mid'

res = requests.get(url)

title = soup.find('title')
title = str(title)

trim = title.split('Sheet music')[0]
trim = trim.rstrip()
if (trim[0] == '<'):
    trim = trim.split('>')[1]

title = trim + '.mid'

with open (title, 'wb') as f:
	f.write(res.content)
