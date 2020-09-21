#score_scraper.py 
#i'm not trying to pay for jacked transcriptions of liscenced works
#Zoe, 2020

from bs4 import BeautifulSoup
from PyPDF2 import PdfFileMerger
import requests
import cairosvg
import img2pdf
import re 
import os
import sys

if (len(sys.argv) == 1):
    score = input("Enter the musecore url for the score you want to download: ")
    r = requests.get(score.rstrip())
elif (len(sys.argv) == 2) :
    r = requests.get(sys.argv[-1])

p = re.compile('score_\d')
soup = BeautifulSoup(r.text, 'html.parser')
page = str(soup)

q = re.search(r'(http|https):\\/\\/([\w]*)\.(([\w]*)\\/){5}(([0-9]*)\\/){4}([\w]*)\\/([\w]*).([\w]{3})', page)
        
source = q.group(0)

sourcefix = ''.join(filter(lambda x: x not in ['\\'], source))

start = sourcefix[:-5] #[...]score_
end = sourcefix[-4:] #.svg

print(end + ' type image')

z = 0
resp = []

while True: 
    url = start + str(z) + end
    res = requests.get(url)
    if (res.status_code != 200) : 
        break
    resp.append(res)
    z+=1

title = soup.find('title')
title = str(title)

trim = title.split('Sheet music')[0]
trim = trim.rstrip()
if (trim[0] == '<'):
    trim = trim.split('>')[1]

y = 0

titles = []
for i in range(0, z):
    titles.append(trim + str(y) + '.pdf')
    y+=1 

if (end == '.svg'):
    for i in range(0, z):
        cairosvg.svg2pdf(resp[i].text, write_to=titles[i])
elif (end == '.png'):
    for i in range(0, z):
        with open(titles[i], 'wb') as f:
            f.write(img2pdf.convert(resp[i].content))

merger = PdfFileMerger()
for pdf in titles:
    merger.append(pdf)

merger.write(trim+'.pdf')
merger.close()

for pdf in titles:
    try:
        os.remove(pdf)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
