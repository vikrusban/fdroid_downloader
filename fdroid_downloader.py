# coding: utf8
import re
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Script to parse F-Droid store apps to repo folder. Python 3.10')
parser.add_argument("-f", help="File with a list of links store", required=True)
args = parser.parse_args()

f = args.f

with open(f) as file:
    array = [row.strip() for row in file]

for i in array:
    resp = requests.get(i)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    links_with_text = []
    for a in soup.find_all('a', attrs={'href': re.compile('^https://f-droid.org/repo/')}):
        if a.text:
            links_with_text.append(a['href'])

    file_for_url = urlparse(links_with_text[1])
    pre_file = file_for_url.path[+1:]
    file = re.sub(r'(_\d{1,254}.apk)', '.apk', pre_file)
    file_check = Path(file_for_url.path[+1:])

    download_file = open(r''+file+'','wb')
    ufr = requests.get(''+links_with_text[1]+'')
    download_file.write(ufr.content)
    download_file.close()
    print('Download: '+links_with_text[1])

print('Done')