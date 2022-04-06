#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
__file__    =  'send.py'
__author__  =  'king'
__time__    =  '2022/04/02 10:08:41'
__version__ =  '1.0'
"""

from oslo_config import cfg
import oslo_messaging as messaging

transport_url = "rabbit://guest:guest@127.0.0.1:5672/"

context = {}
transport = messaging.get_rpc_transport(conf=cfg.CONF, url=transport_url)
target = messaging.Target(topic="test")
client = messaging.RPCClient(transport=transport, target=target)
client = client.prepare()

result = client.call(context, "add", x=1, y=2)
print(f"result is {result}")

client.cast(context, "test")

result = client.call(context, "fib", n=10)
print(f"fib(10) = {result}")
