#-*- coding: utf-8 -*-

import random
import cgi
from wsgiref import simple_server


base = '''<html>
<head>
<title>PyCon APAC 2013 プレゼント抽選システム</title>
</head>
<body>
<form action='.' method='POST'>
<input type="text" name="count" value="%s" />
<input type="submit" name="mode" value="choice" />
</form>
<dl>
%s
</dl>
</body>
</html>
'''


history_tmpl = '''
<dt>
%s
</dt>
<dd>
%s
</dd>
'''


random.seed()


def make_history(histories):

    result = []

    for index, hist in reversed(list(enumerate(histories))):
        result.append(history_tmpl % (index, ', '.join(sorted(hist))))

    return ''.join(result)



def choice(samples, count):

    rest = samples
    choices = set()

    for i in xrange(count):

        c = random.choice(list(rest))

        choices.add(c)
        rest = rest - set([c])

    return rest, choices



class App(object):


    def __init__(self, users):

        self.master = users
        self.available = set(users.keys())
        self.history = []


    def get(self, environ, start_response):

        inp = environ.get('wsgi.input')
        fs = cgi.FieldStorage(fp=inp, environ=environ)

        value = fs.getvalue('count')

        if value is None:
            value = '5'

        start_response('200 OK', [('Content-Type', 'text/html;charset=UTF-8')])

        return [base % (value, make_history(self.history))]


    def post(self, environ, start_response):

        inp = environ.get('wsgi.input')
        fs = cgi.FieldStorage(fp=inp, environ=environ)

        count = int(fs.getvalue('count'))

        rest, choices = choice(self.available, count)

        self.available = rest
        self.history.append(choices)

        start_response('303 See Other', [('Location', '.?count=%s' % count)])

        return ['hello']


    def __call__(self, environ, start_response):

        method = environ.get('REQUEST_METHOD')

        if method.lower() == 'get':
            return self.get(environ, start_response)
        else:
            return self.post(environ, start_response)



def serve(users):

    simple_server.make_server('',  8080, App(users)).serve_forever()

