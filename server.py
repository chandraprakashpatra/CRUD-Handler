import http.server
import socketserver
import json
import os



DATA_FILE = "data.txt"

class CRUDHandler(http.server.SimpleHTTPRequestHandler):

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()  # Fix the typo here

    def do_GET(self):
        if not os.path.exists(DATA_FILE):
            print("Data file not found")
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Data not found"}).encode())
            return

        self._set_headers()
        
        with open(DATA_FILE, 'r') as f:
            data = f.read()
            print("Data read from file:", data)  # Print data for debugging

            # Sending the data as a JSON response
            self.wfile.write(json.dumps({"data": data}).encode())
    #create
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try: 
            data = json.loads(post_data)
            with open(DATA_FILE,"a") as f:
                f.write(f"{data['content']}\n")
            
            self._set_headers(201)
            self.wfile.write(json.dumps({"message":"Data created"}).encode())
        except Exception as e:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error":str(e)}).encode())
    
    def do_PUT(Self):
        content_length = int(self.headers["Content-Length"])
        put_data = self.rfile.read(content_length)

        try:
            new_data = json.loads(put_data)["content"]
            with open(DATA_FILE,w) as f:
                fwrite(f"{new_data}\n")
            
            self._set_headers(200)
            self.wfile.write(json.dumps({"message":"Data updated"}).encode())
        except Exception as e:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error":str(e)}).encode())
    
    def do_DELETE(self):
        if not os.path.exists(DATA_FILE):
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Data not found"}).encode())
            return

        os.remove(DATA_FILE)
        self._set_headers(200)
        self.wfile.write(json.dumps({"message": "Data deleted"}).encode())
    

def run(server_class = http.server.HTTPServer,handler_class = CRUDHandler,port = 8080):
    server_address = ('',port)        
    httpd = server_class(server_address , handler_class)
    print("starting server on {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
