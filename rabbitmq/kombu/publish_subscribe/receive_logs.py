#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__file__    =  'receive_logs.py'
__author__  =  'king'
__time__    =  '2022/03/31 10:43:38'
__version__ =  '1.0'
"""

from kombu import Queue
from kombu import Exchange
from kombu import Connection
from kombu.mixins import ConsumerMixin

exchange = Exchange('log', type='fanout')
queue = Queue('log', exchange=exchange)


class Worker(ConsumerMixin):
    def __init__(self, connection) -> None:
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=[queue],
                callbacks=[self.process_task],
                accept=['text/plain', 'json'],
                prefetch_count=1,
            )
        ]

    def process_task(self, body, message):
        print(body)
        message.ack()


with Connection('amqp://guest:guest@localhost:5672//') as connection:
    try:
        worker = Worker(connection=connection)
        worker.run()
    except KeyboardInterrupt:
        print('bye bye')
