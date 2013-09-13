#-*- coding: utf-8 -*-

from wsgiref import simple_server



class App(object):


    def __init__(self, users):

        self.users = users
        self.history = []


    def get(self, environ, start_response):

        start_response('200 OK', [])

        return [',\n'.join(environ.keys())]


    def post(self, environ, start_response):

        start_response('200 OK', [])

        return ['hello']


    def __call__(self, environ, start_response):

        method = environ.get('REQUEST_METHOD')

        if method.lower() == 'get':
            return self.get(environ, start_response)
        else:
            return self.post(environ, start_response)



def serve(users):

    simple_server.make_server('',  8080, App(users)).serve_forever()



