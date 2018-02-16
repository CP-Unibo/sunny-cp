#!/usr/bin/env python
"""
A simple HTTP server to call sunny-cp.
Examples for sending requests:
    curl -F "--help=" http://localhost:9001
    curl -F "-P=gecode" "mzn=@<FILE>" http://localhost:9001
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import logging
import cgi
import tempfile
import os
import subprocess
import click

# default timeout in seconds for sunny
TIMEOUT = 1200
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        '''
        Handle GET requests.
        '''
        logging.debug('GET %s' % (self.path))
        if urlparse.urlparse(self.path).path == "/solvers":
            self._set_headers()
            solvers_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),os.pardir,"solvers")
            solvers = [name for name in os.listdir(solvers_path) if os.path.isdir(os.path.join(solvers_path, name))]
            self.wfile.write("{}\n".format(",".join(solvers)))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

    def do_HEAD(self):
        self._set_headers()
        
    # def do_POST(self):

    def do_POST(self):
        '''
        Handle POST requests.
        '''
        logging.debug('POST %s' % (self.path))

        # CITATION: http://stackoverflow.com/questions/4233218/python-basehttprequesthandler-post-variables
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = urlparse.parse_qs(self.rfile.read(length))
        else:
            postvars = {}

        # query_values = urlparse.parse_qs(urlparse.urlparse(self.path).query)

        logging.debug('Operation %s' % urlparse.urlparse(self.path).path)
        # logging.debug('Parameters %s' % unicode(query_values))
        # logging.debug('Post data %s' % unicode(postvars))

        if urlparse.urlparse(self.path).path == "/process" or urlparse.urlparse(self.path).path == "/get_features":
            timeout = unicode(TIMEOUT)
            mzn = []
            dzn = []
            extra_param = []
            for i in postvars:
                if i.startswith('mzn'):
                    logging.debug("Found mzn input file")
                    file_id, name = tempfile.mkstemp(suffix='.mzn', text=True)
                    os. write(file_id,''.join(postvars[i]))
                    os.close(file_id)
                    mzn.append(name)
                elif i.startswith('dzn'):
                    logging.debug("Found dzn input file")
                    file_id, name = tempfile.mkstemp(suffix='.dzn', text=True)
                    os.write(file_id, ''.join(postvars[i]))
                    os.close(file_id)
                    dzn.append(name)
                else:
                    if len(postvars[i]) != 1:
                        self.send_response(400)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write("Parameter %s badly formatted" % i)
                        return
                    if postvars[i][0] == "":
                        logging.debug("Found flag %s" % i)
                        extra_param.append(i)
                    else:
                        logging.debug("Found parameter %s with value %s" % (i,postvars[i]))
                        if i == "-T":
                            if "inf" not in postvars[i][0]:
                                timeout = postvars[i][0]
                        extra_param.append(i)
                        extra_param.append(postvars[i][0])

            if urlparse.urlparse(self.path).path == "/process":
                cmd = ["timeout", timeout, "sunny-cp"] + extra_param
                cmd += mzn
                cmd += dzn
            else:
                cmd = ["timeout", timeout, "mzn2feat"] + extra_param
                for i in mzn:
                    cmd += ["-i",i]
                for i in dzn:
                    cmd += ["-d",i]

            logging.debug('Running cmd {}'.format(cmd))
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if process.returncode != 0 and process.returncode != 124:
                logging.debug("The command returned with return code {}. STDOUT <{}>. STDERR <{}>".format(
                    process.returncode,out,err))
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(out)
                self.wfile.write(err)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(out)
            # delete files
            for i in mzn + dzn:
                if os.path.exists(i):
                    os.remove(i)
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()


def run(server_class=HTTPServer, handler_class=MyServer, port=9001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

@click.command()
@click.option('--port', '-p', type=click.INT, default=9001,
              help='Port used by the server to wait for requests.')
def main(port):
    run(port=port)

if __name__ == "__main__":
    main()