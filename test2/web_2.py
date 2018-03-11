#-*- coding:utf-8 -*-
import BaseHTTPServer

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    Page='''\
        <html>
        <body>
        <table>
        <tr> <td>Header </td> <td>Value </td> </tr>
        <tr> <td>Data and time </td> <td>{date_time} </td> </tr>
        <tr> <td>Client host </td> <td>{client_host} </td> </tr>
        <tr> <td>Client port </td> <td>{client_port} </td> </tr>
        <tr> <td>Command </td> <td>{command} </td> </tr>
        <tr> <td>Path </td> <td>{path} </td> </tr>
        </table>
        </body>
        </html>
    '''
    
    def do_GET(self):
        page = self.create_page()
        self.send_content(page)
        
    def create_page(self):
        # wait for realize
        values = {
            'date_time'     : self.date_time_string(),
            'client_host'   : self.client_address[0],
            'client_port'   : self.client_address[1],
            'command'       : self.command,
            'path'          : self.path
        }
        page = self.Page.format(**values)
        return page
        
    def send_content(self, page):
        # wait for realize
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-type", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

# this demo, split do_Get to create_page and send_content, first division.
# and show dynamic html demo.
# there maybe is a issue, visit by chrome return error.
        
if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()    
        
        
        
        
