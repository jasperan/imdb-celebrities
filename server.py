from flask import Flask, jsonify, request
app = Flask(__name__)
import find

@app.route('/imdb')
def imdb_find():
	mode = request.args.get('mode')
	day = request.args.get('day')
	month = request.args.get('month')
	year = request.args.get('year')
