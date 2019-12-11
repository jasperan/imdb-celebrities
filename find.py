from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from sys import exit, argv


def create_driver():
	driver = webdriver.Chrome()
	return driver


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

 
# Auxiliary function to prevent the driver to exit after finishing code execution
def inf_sleep():
	while True:
		sleep(1)


def logout(driver):
	driver.quit()


def main():
	driver = create_driver()

	month = int()
	day = int()
	year = int()
	try:
		month = int(input('Please, introduce your birth month (numerical):'))
		day = int(input('Please, introduce your birth day (numerical):'))
		year = int(input('Please, introduce your birth year (numerical):'))
	except:
		print('Invalid input. Exiting...')
		exit(-1)

	url = 'https://www.imdb.com/search/name/?birth_monthday={}-{}&birth_year={}'.format(
		str(month),
		str(day),
		str(year)
	)

	urls_to_access = execute(driver, url)
	logout(driver)


if __name__ == '__main__':
	main()

