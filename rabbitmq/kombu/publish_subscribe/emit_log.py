#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__file__    =  'emit_log.py'
__author__  =  'king'
__time__    =  '2022/03/31 10:32:30'
__version__ =  '1.0'
"""

from kombu import Connection
from kombu import Exchange

exchange = Exchange('log', type='fanout')

with Connection('amqp://guest:guest@localhost:5672//') as connection:
    producer = connection.Producer()
    for i in range(10):
        producer.publish(
            body=f'INFO: {i + 1}th message',
            routing_key='',
            exchange=exchange,
            declare=[exchange],
        )
