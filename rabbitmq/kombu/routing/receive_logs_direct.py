#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__file__    =  'receive_logs_direct.py'
__author__  =  'king'
__time__    =  '2022/03/31 11:25:15'
__version__ =  '1.0'
"""
from kombu import Queue
from kombu import Exchange
from kombu import Connection
from kombu.mixins import ConsumerMixin

levels = ['INFO', 'ERROR', 'WARNING']
exchange = Exchange('direct_logs', type='direct')
queues = [
    Queue(f'log.{level}', exchange=exchange, routing_key=level)
    for level in levels
]


class Worker(ConsumerMixin):
    def __init__(self, connection) -> None:
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=queues,
                accept=['text/plain', 'json'],
                callbacks=[self.process_task],
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
