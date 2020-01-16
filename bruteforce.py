from bs4 import BeautifulSoup
from sys import exit, argv
import requests
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError


def initialize_db():

	ADDRESS = '127.0.0.1' #'belainstance-20190506-1152'  
	PORT = '3306'
	USERNAME = 'root'
	PASSWORD = 'p/Me8*Aq'
	# Old user:pass from old machine's database.
	# POSTGRES_USERNAME = 'bbvabe'     
	# POSTGRES_PASSWORD = 'alvaro$$2019' 
	DBNAME = 'wraith'

	# A long string that contains the necessary Postgres login information
	postgres_str = ('mysql://{username}:{password}@{ipaddress}:{port}/{dbname}'
	                .format(username=USERNAME, 
	                        password=PASSWORD,
	                        ipaddress=ADDRESS,
	                        port=PORT,
	                        dbname=DBNAME))

	# Create the connection
	
	cnx = create_engine(postgres_str)
	connection = cnx.connect()

		
	return connection


def call_db(connection, data):
	sql = "INSERT INTO actors values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}) * from aa;".format(
		data.get('url'),
		data.get('name'),
		data.get('knownfor_1'),
		data.get('knownfor_2'),
		data.get('knownfor_3'),
		data.get('birthday'),
		data.get('rank'),
		data.get('famous_title_1'),
		data.get('famous_title_2'),
		data.get('famous_title_3'),
		data.get('alive')
	)
	try:
		result = connection.execute(sql)
		for i in result:
			print('Row: %s' % i)
	except:
		return # Means that the values were already inserted


def destroy_session(connection):
	connection.close()


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

	actor_name = str()
	knownfor_list = list()

	for i in range(len(obj)):
		iteration = obj[i].string.lstrip('\n').rstrip('\n')
		if i == 0:
			actor_name = iteration
			print('Actor Name: {}'.format(iteration))
		else:
			knownfor_list.append(iteration)
			print('Known For: {} ({}/{})'.format(iteration,
				i,
				len(obj)-1)
			)
	ranking = str()
	obj = soup.find(id='meterRank')
	if obj.string == 'SEE RANK':
		obj = 'Below Rank 5000'
	else:
		obj = obj.string
	ranking = obj
	print('MeterRank: {}'.format(
		obj))

	prepare_data = dict()
	prepare_data['url'] = url
	prepare_data['name'] = actor_name
	for i in range(len(knownfor_list)):
		prepare_data['knownfor_{}'.format(i+1)] = knownfor_list[i]

	prepare_data['rank'] = ranking
	# TODO
	prepare_data['birthday'] = 'TODO'
	for i in range(3):
		prepare_data['famous_title_{}'.format(i+1)] = 'TODO'
	prepare_data['alive'] = -1


	connection = initialize_db()
	call_db(connection, prepare_data)
	destroy_session(connection)


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

