#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__file__    =  'emit_log_direct.py'
__author__  =  'king'
__time__    =  '2022/03/31 11:15:12'
__version__ =  '1.0'
"""


from kombu import Exchange
from kombu import Connection

levels = ['INFO', 'ERROR', 'WARNING']
exchange = Exchange('direct_logs', type='direct')


with Connection('amqp://guest:guest@localhost:5672//') as connection:
    producer = connection.Producer()
    for i in range(1, 20):
        level = levels[i % len(levels)]
        log = f'{level}: {i}th message'
        producer.publish(
            body=log,
            routing_key=level,
            exchange=exchange,
            declare=[exchange],
        )
