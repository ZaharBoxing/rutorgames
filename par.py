#!/usr/bin/env python3

import csv
import urllib.request 
from bs4 import BeautifulSoup

BASE_URL = 'http://the-rutor.org/games/'

def get_html(url):
	response = urllib.request.urlopen(url)
	return response.read()

def get_page_count(html):
	soup = BeautifulSoup(html, 'lxml')
	paggination = soup.find('p', align='center')
	for a in paggination.find_all(('a')[-1]):
		b = a.find_all('b')[-1].text.replace(u'\xa0',' ')
	return int(int(b[7:])/100)

def parse(html):
	soup = BeautifulSoup(html, 'lxml')
	div = soup.find('div', id='index')
	projects = []

	for row in div.find_all('tr')[1:]:
		cols = row.find_all('td')
		
		projects.append({
			'date': cols[0].text.replace(u'\xa0',' '),
			'title': cols[1].text.strip(),
			'value': cols[3].text.replace(u'\xa0',' ')
		})

	return projects

def save(projects, path):
	with open(path, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(('Дата', 'Название', 'Вес'))

		for project in projects:
			writer.writerow((project['date'], project['title'], project['value']))


def main():
	page_count = get_page_count(get_html(BASE_URL))
	print('Всего страниц %d' % page_count)

	projects = []

	for page in range(1, page_count):
		print('Парсинг в процессе')
		projects.extend(parse(get_html('http://the-rutor.org/' + 'browse/%d/8/0/0/' % page)))


	save(projects, 'rutorgames.csv')


if __name__ == '__main__':
	main()