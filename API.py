import redis, base64, md5, config, sys

class URL_Shortener:
    def __init__(self):
        self.redis = redis.StrictRedis(host=config.REDIS_HOST,
                                       port=config.REDIS_PORT,
                                       db=config.REDIS_DB)

    def shortcode(self, url):
        return base64.b64encode(md5.new(url).digest()[-4:]).replace('=','').replace('/','_')

    def shorten(self, url):
        code = self.shortcode(url)
        try:
            self.redis.set(config.REDIS_PREFIX + code, url)
            return {'success': True,
                    'url': url,
                    'code': code,
                    'shorturl': config.URL_PREFIX + code}
        except:
            return {'success': False}

    def lookup(self, code):
        try:return self.redis.get(config.REDIS_PREFIX + code)
        except:return None
 
from flask import flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Shorten(Resource):
	def get(self, url):
		return {"Shortened Url":URL_Shortener.shorten(url)}

	def post(self, url): #subject to change
		return {"Lookup":URL_Shortener.lookup(url)}

api.add_resource(Shorten, "/shortenlink/<string:url>")
api.add_resource(Shorten, "/lookuplink/<string:url>") #subject to change

if __name__=="__main__":
	app.run(debug = True)