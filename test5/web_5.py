#-*- coding:utf-8 -*-
import BaseHTTPServer, os, sys, subprocess

#---------

class ServerException(Exception):
    pass

#---------

class base_case(object):

    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')
        
    def test(self, handler):
        assert False, 'Not implemented.'
    
    def act(self, handler):
        assert False, 'Not implemented.'
    
class case_no_file(base_case):
    def test(self, handler):
        return not os.path.exists(handler.full_path)
    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))

class case_cgi_file(base_case):
    def run_cgi(self, handler):
        data = subprocess.check_output(["python", handler.full_path])
        handler.send_content(data)
    
    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
            handler.full_path.endswith('.py')
    
    def act(self, handler):
        self.run_cgi(handler)
        
class case_existing_file(base_case):
    def test(self, handler):
        return os.path.isfile(handler.full_path)
    def act(self, handler):
        self.handle_file(handler, handler.full_path)
    
class case_directory_index_file(base_case):
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               os.path.isfile(self.index_path(handler))
    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))

class case_always_fail(base_case):
    def test(self, handler):
        return True
    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))
        

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    Cases = [case_no_file(),
        case_cgi_file(),
        case_existing_file(),
        case_directory_index_file(),
        case_always_fail()]
    # here is one issue, order is very important.
    Error_Page = '''\
    <html>
    <body>
    <h1>Error accessing</h1>
    <p>{msg}</p>
    </body>
    </html>
    '''
    
    def do_GET(self):
        try:
            self.full_path = os.getcwd().replace('\\','/') + self.path
            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)
            
    def handle_error(self, msg):
        content = self.Error_Page.format(path = self.path, msg=msg)
        self.send_content(content, 404)
        
    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)
    


# just divide something from do_GET, add too many codes.
# but, this make code clear, one class do one thing.
            
if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()  
