#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
__file__    =  'receive.py'
__author__  =  'king'
__time__    =  '2022/04/02 10:36:52'
__version__ =  '1.0'
"""

import time
from oslo_config import cfg
import oslo_messaging as messaging

transport_url = "rabbit://guest:guest@127.0.0.1:5672/"


class Endpoint(object):
    def _fib(self, n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self._fib(n - 1) + self._fib(n - 2)

    def fib(self, context, n):
        print(n)
        return self._fib(n)

    def test(self, context):
        print("testing")

    def add(self, context, x, y):
        result = x + y
        print(f"result is {result}")
        return result


transport = messaging.get_rpc_transport(conf=cfg.CONF, url=transport_url)
target = messaging.Target(topic="test", server="server-1")
endpoints = [Endpoint()]
server = messaging.get_rpc_server(transport, target, endpoints=endpoints)
try:
    print("Start Server")
    server.start()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping Server")
    server.stop()
    server.wait()
