#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__file__    =  'send.py'
__author__  =  'king'
__time__    =  '2022/03/28 11:23:00'
__version__ =  '1.0'
"""

import kombu
import datetime


if __name__ == "__main__":
    with kombu.Connection("amqp://guest:guest@localhost:5672//") as conn:
        simple_queue = conn.SimpleQueue("hello")
        message = f"helloworld, sent at {datetime.datetime.today()}"
        simple_queue.put(message)
        print(f"Sent: {message}")
        simple_queue.close()
