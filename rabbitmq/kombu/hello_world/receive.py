#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__file__    =  'receive.py'
__author__  =  'king'
__time__    =  '2022/03/28 14:56:22'
__version__ =  '1.0'
"""

import kombu

with kombu.Connection('amqp://guest:guest@localhost:5672//') as conn:
    simple_queue = conn.SimpleQueue('hello')
    message = simple_queue.get(block=True, timeout=1)
    print(f'Received: {message.payload}')
    message.ack()
    simple_queue.close()
