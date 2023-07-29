import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# In-memory data store for employees
employees_data = {}

# HTTP request handler
class EmployeeRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/employees':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(list(employees_data.values())).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

    def do_POST(self):
        if self.path == '/employees':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            employee_data = json.loads(post_data)
            emp_id = employee_data.get('emp_id')
            if emp_id not in employees_data:
                employees_data[emp_id] = employee_data
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Employee added successfully'}).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Employee already exists'}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

def run_server():
    host = 'localhost'
    port = 8000
    server_address = (host, port)
    httpd = HTTPServer(server_address, EmployeeRequestHandler)
    print(f'Starting server at http://{host}:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
