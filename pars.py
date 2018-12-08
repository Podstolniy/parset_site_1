#!/usr/bin/env python
#-*- coding: utf-8 -*-
import urllib.request
import re
from bs4 import BeautifulSoup

TEST_URL = 'https://www.lueftner-cruises.com/en/river-cruises/cruise.html'

def get_html(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    request = urllib.request.Request(url, headers = {'User-Agent': user_agent})
    response = urllib.request.urlopen(request)
    return response.read()

def parse(html):
    soup = BeautifulSoup (html,'html.parser')
    table = soup.find('div', class_='content')
    urls = []
    for item in table.find_all('a'):
        urls.append ('https://www.lueftner-cruises.com'+item.get('href'))
    ur = []
    for i in urls:
        if i not in ur:
           ur.append(i) 
    return ur[:4]

def parse_page(html):
    url_pages = []
    for i in html:
        soup = BeautifulSoup (get_html(i),'html.parser')
        table = soup.find('div', class_='col-md-9 river-site-highlight')
        table1 = soup.find('div', class_='col-lg-5 col-md-6 col-sm-12 col-xs-12')
        table2 = soup.find('div',class_='panel-group accordion route')
        table3 = soup.find('div',class_='panel-group accordion price accordeon-data-price')
        url_pages.append({
            'name':[names.text.strip() for names in table.find_all('h1')],
            'days':[names.text.strip() for names in table1.find_all('p')][1:],
            'itinerry':[names.text.split() for names in table2.find_all('span', class_='route-city')],
            'dates':[names.text.strip() for names in table3.find_all('div', class_='price-date')],
            'ship':[names.text.strip() for names in table3.find_all('span', class_='table-ship-name')],
            'price':[names.text.strip() for names in table3.find_all('span', class_='big-table-font')],
        })

    return (url_pages)
def main():
    url_all = parse(get_html(TEST_URL))
    print(parse_page([a for a in url_all]))

if __name__ == '__main__':
    main()
