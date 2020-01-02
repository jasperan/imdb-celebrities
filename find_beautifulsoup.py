from bs4 import BeautifulSoup
from sys import exit, argv
import requests


def execute(driver, url):
	actors_urls = list()
	driver.get(url)

	try:
		element = driver.find_elements_by_xpath('//h3[@class="lister-item-header"]/a')
	except:
		print('Exception')
	finally:
		print('Found it')
		print(str(len(element)))

	for i in range(len(element)):
		actors_urls.append(element[i].get_attribute('href'))
		print('Iteration {}: {}'.format(i+1, element[i].get_attribute('href')))
		print('Name: {}'.format(element[i].text))

	return actors_urls

def main(mode='default', day='11', month='12', year='1996'):

	url = 'https://www.imdb.com/search/name/?birth_monthday={}-{}&birth_year={}'.format(
		str(month),
		str(day),
		str(year)
	)
	list_names = list()
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')
	# print(soup.prettify())
	obj = soup.find_all('h3')
	print(obj)
	print('Found {} elements'.format(
		len(obj)))
	for i in range(len(obj)):
		try:
			print(obj[i].find('a').get('href'))
			print(obj[i].find('a').string)
			list_names.append(obj[i].find('a').string.rstrip())
		except AttributeError:
			print('Element {} was empty: {}'.format(
				i+1,
				obj[i]))
	print('List of Names: {}'.format(
		list_names))
	return list_names



if __name__ == '__main__':
	main()

