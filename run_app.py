"""
just for debugging utility in pycharm to run app.py
"""
# pylint: disable=missing-docstring,invalid-name

from wsgiref import simple_server
import os
import subprocess
import urllib3

from look.app import api

urllib3.disable_warnings()

if __name__ == '__main__':
    subprocess.call(
        "lsof -i -P -n | grep LISTEN | grep 8000 | awk '{print $2}' | xargs kill -9; sleep 5",
        shell=True)
    httpd = simple_server.make_server('0.0.0.0', 8000, api)
    httpd.serve_forever()
