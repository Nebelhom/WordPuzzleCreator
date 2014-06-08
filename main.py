from flask import Flask, render_template, jsonify, request, Response, send_file
app = Flask(__name__)
app.config['DEBUG'] = True

import json
import logging
import mimetypes
import StringIO
from werkzeug.datastructures import Headers
import zipfile

# word puzzle
import wordpuzzle

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def start_page():
	puzzles = [
		dict(btn_label='Search the Word!', ID='wordsearchbtn', href='./wordsearch'),
		]
	return render_template('index.html', puzzles=puzzles)

@app.route('/about')
def about_page():
	return render_template('about.html')

@app.route('/_create_wordsearch.xls', methods=['POST'])
def create_wordsearch():

	wordlist = request.form.getlist('wordlist')

	# create a stringIO object
	output = StringIO.StringIO()

	# Instantiate the PuzzleGrid class
	p = wordpuzzle.PuzzleGrid(wordlist)
	# Create the Puzzle
	p.main()

	# Create file in memory
	p.output2excel(output)
	mime = 'application/vnd.ms-excel'

	# Set back to start
	output.seek(0)

	# send back to client
	return send_file(output, mimetype=mime)

@app.route('/wordsearch')
def wordsearch():
	"""GUI to create wordsearch puzzle"""
	return render_template('wordsearch.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404