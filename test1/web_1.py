#-*- coding:utf-8 -*-
import BaseHTTPServer

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    Page = '''\
        <html>
        <body>
        <p>Hello, web!</p>
        </body>
        </html>
    '''
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(self.Page)))
        self.end_headers()
        self.wfile.write(self.Page)

# this demo, just show how to use BaseHTTPServer handle HTTP request.         
        
if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
