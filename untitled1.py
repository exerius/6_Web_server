import http.server

class myHandler(http.server.SimpleHTTPRequestHandler):
    def log_request(self, code="-", size="-"):
        try:
            code = code.value
        except:
            code = str(code)
        self.log_message('"%s" %s', str(self.requestline.split(" ")[1]), str(code))
    def log_message(self, format, *args):
        with open("log.txt", "a") as file:
            file.write("%s - - %s %s\n" % (self.log_date_time_string(), self.address_string(), format%args))
    def do_POST():
        path = self.translate_path(self.path)
        length = int(self.headers['Content-Length'])
        with open(path, 'wb') as f:
            f.write(self.rfile.read(length))
        self.send_response(201, "Created")
    def do_PUT():
        self.do_POST()
    
PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler
with http.server.ThreadingHTTPServer(("", 8001), myHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()