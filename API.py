from flask import Flask
from flask_restful import Api, Resource
import re, random
from base64 import b64encode
from hashlib import blake2b

def url_valid(url):
	regex = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	return re.match(regex, url) is not None

def shorten(url, size):
	global shortened
	DIGEST_SIZE = size
	shortened = {}
	url_hash = blake2b(str.encode(url), digest_size=DIGEST_SIZE)
	while url_hash in shortened:
		url += str(random.randint(0, 9))
		url_hash = blake2b(str.encode(url), digest_size=DIGEST_SIZE)
	b64 = b64encode(url_hash.digest(), altchars=b'-_')
	return b64.decode('utf-8')

def bad_request(message):
    response = {'message': message}
    status_code = 400
    return response, status_code

def shorten_url(url, size):
	if url[:4] != 'http':
		url = 'http://' + url

	if not url_valid(url):
		return bad_request('Provided url is not valid.')

	shortened_url = shorten(url, size)
	return {'shortened_url': shortened_url}, 201

app = Flask(__name__)
api = Api(app)

class Main(Resource):
	def get(self, size, url):
		return {"Success": True,9
				"Initial Url":url,
				"Digest Size":size,
				"Shortened Url": shorten_url(url, size)}

api.add_resource(Main, "/shortenlink/<int:size>/<path:url>") 

if __name__== '__main__':
	app.run(debug=True)
