#!/usr/bin/env python3

"""

Scrapes sector and industry data from finviz.

Usage:
    python3 finviz_sector_scraper.py

Matthew Morrish

"""


#Imports
import requests, time, random
from bs4 import BeautifulSoup


# Get number of pages to scrape data from
def __getNumPages(url):

	# Make a request & soup it
	headers = {'User-Agent': 'Mozilla/5.0'}
	html = requests.get(url, headers=headers)
	soup = BeautifulSoup(html.content, "html.parser")

	# Extract what we need & clean it up
	count = str(soup.find('td', class_ = 'count-text').get_text())
	count = count.split(' ')[1]
	
	return int(count)


# Extracts the ticker/sector/industry data from url
def __getData(url):

	# Make a request & soup it
	headers = {'User-Agent': 'Mozilla/5.0'}
	html = requests.get(url, headers=headers)
	soup = BeautifulSoup(html.content, "html.parser")

	# Filter down to useful data & parse it into a list
	main_div = soup.find('div', attrs={'id': 'screener-content'})
	table = main_div.find('table')
	sub = table.findAll('tr')
	rows = sub[5].findAll('td')
	data = [row.a.get_text() for row in rows if row.a != None]
	del data[0]

	# Break data up into sublists by rows
	data_li, sub_li = [], []
	for i in range(len(data)):
		if i % 11 == 0 and i != 0:
			data_li.append(sub_li)
			sub_li = []
		sub_li.append(data[i])
	data_li.append(sub_li)

	# Parse to a dict and return
	return {row[1] : {'sector': row[3], 'industry': row[4]} for row in data_li}


# Main
def scrape():

	# Set some vars
	base_url = 'https://finviz.com/screener.ashx?v=111&f=geo_usa'
	info_per_page = 20
	numPgSize = __getNumPages(base_url)
	human_params = (1.5, 3.5)

	# Find out how many pages there are then generate all the urls we need to scrape
	url_qty = int((numPgSize - (numPgSize % info_per_page)) / info_per_page)
	urls = [base_url] + [base_url + '&r=' + str(i*info_per_page+1) for i in range(1, url_qty+1)]

	# For each url, get its data and add it to results
	results = {}
	for i in urls:
		time.sleep(random.uniform(human_params[0], human_params[1]))
		results.update(__getData(i))

	return results


if __name__ == '__main__':
	results = scrape()
	print(results)