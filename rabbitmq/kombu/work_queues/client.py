#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__file__    =  'send.py'
__author__  =  'king'
__time__    =  '2022/03/28 16:50:40'
__version__ =  '1.0'
"""
from kombu import Queue
from kombu import Connection

queue = Queue('task_queue', routing_key='task_queue')

with Connection('amqp://guest:guest@localhost:5672//') as connection:
    producer = connection.Producer()
    for i in range(1, 11):
        producer.publish(
            body=f'{i}th message',
            routing_key='task_queue',
            queue=queue,
            declare=[queue],
        )
