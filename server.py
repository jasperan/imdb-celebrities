from flask import Flask, jsonify, request
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
import find_beautifulsoup

@app.route('/imdb')
def imdb_find():
	mode = request.args.get('mode')
	day = request.args.get('day')
	month = request.args.get('month')
	year = request.args.get('year')

	error_json = {
		'error_code':int(),
		'error_description':str()
	}

	if mode not in ['default', 'month']:
		print('Invalid mode selected')
		error_json['error_code'] = -1
		error_json['error_description'] = 'Invalid mode selected'
		return error_json
	elif int(day) not in range(1, 32):
		print('Invalid day selected')
		error_json['error_code'] = -2
		error_json['error_description'] = 'Invalid day selected'
	elif int(month) not in range(1, 13):
		error_json['error_code'] = -3
		error_json['error_description'] = 'Invalid month selected'
	elif int(year) not in range(0, 2021):
		error_json['error_code'] = -4
		error_json['error_description'] = 'Invalid year selected'

	result = find_beautifulsoup.main(mode, day, month, year)
	return jsonify(result)


