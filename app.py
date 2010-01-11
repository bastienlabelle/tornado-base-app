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
from tornado.options import define, options


import os
import sys

define('version', default=None,help='Version settings (default: production)')

class App(tornado.web.Application):
	def __init__(self,settings):
		handlers = [
			(r'/', MainHandler)
		]
		
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
		print 'Invalid or missing config file %s' % __config__
	
	# if no settings, we go away
	if 'settings' not in config:
		print 'No default configuration found'
		sys.exit(1)
	
	if options.version and options.version in config['extra_settings']:
		settings = dict(
			config['settings'],
			**config['extra_settings'][options.version]
		)
	else:
		settings = config['settings']
	
	for k,v in settings.items():
		if k.endswith('_path'):
			settings[k] = settings[k].replace(
				'__path__',
				os.path.dirname(__file__)
			)
	
	http_server = tornado.httpserver.HTTPServer(App(settings))
	http_server.listen(config['port'])
	if 'debug' in settings and settings['debug'] is True:
		tornado.autoreload.start()
	tornado.ioloop.IOLoop.instance().start()