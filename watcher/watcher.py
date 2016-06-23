# watcher.py
#
# Copyright (c) 2016 Michael Jiang
# This file is part of git-watcher under
# the MIT License: https://opensource.org/licenses/MIT

# !/usr/bin/env python

import argparse
import hashlib
import hmac
import json
import os
import subprocess
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import sys

import signal

__version__ = '0.4'
current_dir = os.path.dirname(__file__)

parser = argparse.ArgumentParser(description='git-watcher', version=__version__, prog='git-watcher')

parser.add_argument('-i', action='store', dest='ip', default='0.0.0.0', help='listen ip address')
parser.add_argument('-p', action='store', dest='port', default=8000, help='listen port', type=int)
parser.add_argument('-u', action='store', dest='repo_url', help='git repository url', required=True)
parser.add_argument('-b', action='store', dest='branch', default='master', help='watch branch')
parser.add_argument('-s', action='store', dest='secret', help='secret key of webhook', required=True)
parser.add_argument('-d', action='store', dest='dir', default=current_dir, help='local repository directory')

options = None


class Validator(object):
    def __init__(self):
        self.secret = options.secret
        self.digest_maker = hmac.new(self.secret, '', hashlib.sha1)

    def validate(self, body, sha1):
        if body is None or sha1 is None:
            return False

        self.digest_maker.update(body)
        return self.digest_maker.hexdigest() == sha1


class WebhookHandler(BaseHTTPRequestHandler):
    watcher = None
    validator = None

    def do_POST(self):
        headers = self.headers
        event = headers.get('X-GitHub-Event')
        if event is None or event != 'push':
            print 'not push event, not rebuild'
            self.response("not push event")
        else:
            sig = headers.get('X-Hub-Signature')
            data = self.rfile.read(int(self.headers['content-length']))
            self.initialize()
            if WebhookHandler.validator.validate(data, sig[sig.find('=') + 1:]):
                WebhookHandler.watcher.update()
                self.response("ok")
            else:
                print 'validation failed, not rebuild'
                self.response('validate fail')

    def response(self, message):
        message = {'result': message}
        self.send_response(code=200)
        self.send_header('Content-Type', 'application-json')
        self.end_headers()
        self.wfile.write(json.dumps(message))

    @classmethod
    def initialize(cls):
        if hasattr(cls, 'watcher'):
            WebhookHandler.watcher = GitWatcher()
        if hasattr(cls, 'validator'):
            WebhookHandler.validator = Validator()


class WebhookWatcher(HTTPServer):
    def __init__(self, request_handler):
        self.ip = options.ip
        self.port = options.port
        HTTPServer.__init__(self, (self.ip, self.port), request_handler)

    def start(self):
        print 'git watcher is listen on %s:%d' % (self.ip, self.port)
        self.serve_forever()


class GitWatcher(object):
    def __init__(self):
        self.origin_url = options.repo_url
        self.repo_name = options.repo_url[options.repo_url.rfind('/') + 1:options.repo_url.rfind('.')]
        self.branch = options.branch
        self.save_dir = options.dir
        self.full_path = os.path.join(self.save_dir, self.repo_name)

    def clone(self):
        print "starting clone..."
        try:
            subprocess.check_call(["git", "clone", self.origin_url, "-b", self.branch], cwd=self.save_dir)
            print "clone completed!"
        except subprocess.CalledProcessError as err:
            print 'ERROR:', err

    def exist(self):
        return os.path.exists(os.path.join(self.save_dir, self.repo_name))

    def pull(self):
        print "pulling repository..."
        try:
            subprocess.check_call(["git", "pull"], cwd=self.full_path)
            print "pull repository completed!"
        except subprocess.CalledProcessError as err:
            print 'ERROR:', err

    def update(self):
        if not self.exist():
            self.clone()
        else:
            self.pull()


def exit(signal, frame):
    sys.exit(0)


def run():
    global options
    options = parser.parse_args()

    signal.signal(signal.SIGINT, exit)

    webhook_watcher = WebhookWatcher(WebhookHandler)
    webhook_watcher.start()


if __name__ == '__main__':
    run()
