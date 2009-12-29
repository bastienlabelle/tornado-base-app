#! /usr/bin/env python
# *-* coding: utf8 *-*

__author__ = 'Bastien Labelle'
__email__ = 'hello@bastienlabelle.fr'
__date__ = '2009-12-28'
__appname__ = 'app.py'
__version__ = 0.1
__config__ = 'app.yaml'

import optparse
import yaml

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.auth
import tornado.options
import tornado.autoreload

import os
import sys

class App(tornado.web.Application):
	def __init__(self,config):
		handlers = [
			(r'/', MainHandler)
		]
		settings = {
			'static_path' : os.path.join(
				os.path.dirname(__file__),
				config['static_path']
			),
			'template_path' : os.path.join(
				os.path.dirname(__file__),
				config['template_path']
			),
			'cookie_secret' : config['cookie_secret'],
			'xsrf_cookies' : config['xsrf_cookies'],
			'version' : __version__
		}
		
		tornado.web.Application.__init__(
			self,
			handlers,
			settings
		)

class BaseHandler(tornado.web.RequestHandler):
	pass

class MainHandler(BaseHandler):
	def get(self):
		self.write('Hello world!')
		self.finish()

if __name__ == '__main__':
	tornado.options.parse_command_line()
	
	try:
		f = file(__config__, 'r')
		config = yaml.load(f)
		f.close()
	except IOError:
		print 'Invalid or missing config file %s' % options.config
		sys.exit(1)
	
	#print config
		
	
	http_server = tornado.httpserver.HTTPServer(App(config))
	http_server.listen(config['port'])
	if config['debug']:
		tornado.autoreload.start()
	tornado.ioloop.IOLoop.instance().start()