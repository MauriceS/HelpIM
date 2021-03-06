#!/usr/bin/python
# vim: set fileencoding=utf-8

# Based upon
# http://mail.python.org/pipermail/python-list/2003-June/210343.html

import BaseHTTPServer, select, socket, SocketServer, urlparse
from django.core.management.base import BaseCommand

class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    __base = BaseHTTPServer.BaseHTTPRequestHandler
    __base_handle = __base.handle

    rbufsize = 0                        # self.rfile Be unbuffered

    def handle(self):
        self.__base_handle()

    def _connect_to(self, netloc, soc):
        i = netloc.find(':')
        if i >= 0:
            host_port = netloc[:i], int(netloc[i+1:])
        else:
            host_port = netloc, 80
        print "\t" "connect to %s:%d" % host_port,
        try: soc.connect(host_port)
        except socket.error, arg:
            try: msg = arg[1]
            except: msg = arg
            self.send_error(404, msg)
            return 0
        return 1

    def do_GET(self):
        (scm, _, path, params, query, fragment) = urlparse.urlparse(self.path, 'http')
        if self.path == '/http-bind/':
            print "JABBER:",
            netloc = "127.0.0.1:5280"
        else:
            print "DJANGO:",
            netloc = "127.0.0.1:8000"

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(netloc, soc):
                self.log_request()
                soc.send("%s %s %s\r\n" % (
                    self.command,
                    urlparse.urlunparse(('', '', path, params, query, '')),
                    self.request_version))
                self.headers['Connection'] = 'close'
                for key_val in self.headers.items():
                    soc.send("%s: %s\r\n" % key_val)
                soc.send("\r\n")
                self._read_write(soc)
        finally:
            soc.close()
            self.connection.close()

    def _read_write(self, soc, max_idling=20000):
        iw = [self.connection, soc]
        ow = []
        count = 0
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, ow, iw, 3)
            if exs: break
            if ins:
                for i in ins:
                    if i is soc:
                        out = self.connection
                    else:
                        out = soc
                    data = i.recv(8192)
                    if data:
                        out.send(data)
                        count = 0
            else:
                print "..", count,
            if count == max_idling: break

    do_HEAD =  do_GET
    do_POST =  do_GET
    do_PUT  =  do_GET
    do_DELETE= do_GET

class ThreadingHTTPServer (SocketServer.ThreadingMixIn,
                           BaseHTTPServer.HTTPServer): pass

class Command(BaseCommand):
    help = "runs a transparent proxy to forward BOSH requests to local jabber server (development only!)"

    def handle(self, *args, **options):
        server_address = ('', 8888)
        httpd = ThreadingHTTPServer(server_address, ProxyHandler)
        print "Starting transparent proxy at http://127.0.0.1:8888/"
        httpd.serve_forever()
        
