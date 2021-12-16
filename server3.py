import http.server
import os


class myHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.directory = os.fspath(dirname)
        super().__init__(*args, **kwargs)

    def log_request(self, code="-", size="-"):
        try:
            code = code.value
        except:
            code = str(code)
        self.log_message('"%s" %s', str(self.requestline.split(" ")[1]), str(code))

    def log_message(self, format, *args):
        with open("log.txt", "a") as file:
            file.write("%s - - %s %s\n" % (self.log_date_time_string(), self.address_string(), format%args))

    def do_HEAD(self):
        if (len(bytes(self.requestline.encode() + str(self.headers).encode()))) <= leng:
            super().do_HEAD()

    def do_GET(self):
        if ((len(bytes(self.requestline.encode()+str(self.headers).encode()))) <= leng) and (self.requestline[1][:-3] in allowed):
            super().do_GET()
        else:
            self.send_error(403


    def do_POST(self):
        if (len(bytes(self.requestline.encode()+str(self.headers).encode()))) <= leng:
            super().do_GET()
            path = self.translate_path(self.path)
            length = int(self.headers['Content-Length'])
            with open(path, 'wb') as f:
                f.write(self.rfile.read(length))
            self.send_response(201, "Created")

    def do_PUT(self):
        if (len(bytes(self.requestline.encode()+str(self.headers).encode()))) <= leng:
            super().do_GET()
        self.do_POST()


with open("settings.txt", "r") as file:
    settings = []
    for i in file:
        settings.append(i.split(":"))
    settings = {i[0]: i[1] for i in settings}
    PORT = int(settings["socket"])
    dirname = settings["dir"]
    leng = int(settings["leng"])
    allowed = [".html", ".css", ".js", ".ico"]


Handler = http.server.SimpleHTTPRequestHandler
with http.server.ThreadingHTTPServer(("", PORT), myHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
