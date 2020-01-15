from bs4 import BeautifulSoup
from sys import exit, argv
import requests
import time

def parse_people(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')

	obj = soup.find(id='meterRank')
	if obj.string == 'SEE RANK':
		obj = 'Below Rank 5000'
	else:
		obj = obj.string
	print('MeterRank: {}'.format(
		obj))

	obj_2 = soup.find(id='knownfor')
	'''
	print('Known for: {}'.format(
		obj_2))
	'''
	obj_3 = obj_2.find_all('span', class_='knownfor-ellipsis')
	obj_4 = obj_2.find_all('a', class_='knownfor-ellipsis')
	obj_5 = obj_2.find_all(class_='knownfor-year')

	list_titles = list()
	list_years = list()
	list_roles = list()

	for i in range(0, len(obj_3), 2):
		list_titles.append(obj_3[i].string)
	for i in range(1, len(obj_3), 2):
		list_years.append(obj_3[i].string)
	for i in range(len(obj_4)):
		list_roles.append(obj_4[i].string)

	print('{} // {} // {}'.format(
		list_titles,
		list_roles,
		list_years))

	assert len(list_titles) == len(list_roles) == len(list_years)


	list_returner = list()
	for i in range(len(list_titles)):
		dictionary = {
			'title':list_titles[i],
			'role':list_roles[i],
			'year':list_years[i]
		}
		list_returner.append(dictionary)

	return list_returner


def bruteforce(iteration):
	correct_number = format(iteration, '07d')
	url = 'https://www.imdb.com/name/nm{}'.format(correct_number)
	print('Accessing URL: {}'.format(url))

	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')
	# print(soup.prettify())
	obj = soup.find_all('span', class_='itemprop')

	if not obj:
		print('Iteration {} did not match any results.'.format(correct_number))
		return

	for i in range(len(obj)):
		iteration = obj[i].string.lstrip('\n').rstrip('\n')
		if i == 0:
			print('Actor Name: {}'.format(iteration))
		else:
			print('Known For: {} ({}/{})'.format(iteration,
				i,
				len(obj)-1)
			)

	obj = soup.find(id='meterRank')
	if obj.string == 'SEE RANK':
		obj = 'Below Rank 5000'
	else:
		obj = obj.string
	print('MeterRank: {}'.format(
		obj))

	'''
	print('Found {} elements'.format(
		len(obj)))
	for i in range(len(obj)):
		try:
			href = obj[i].find('a').get('href')
			name = obj[i].find('a').string.rstrip()
			parsed_info = parse_people('{}{}'.format(
				'https://imdb.com',
				href))
			iteration_dict = {
				'name':name,
				'url':href,
				'information':parsed_info
			}
			print(href)
			print(name)
			list_obj.append(iteration_dict)
		except AttributeError:
			print('Element {} was empty: {}'.format(
				i+1,
				obj[i]))
	print('Objects: {}'.format(
		list_obj))

	return list_obj
	'''



if __name__ == '__main__':
	for i in range(9999999):
		bruteforce(i)

