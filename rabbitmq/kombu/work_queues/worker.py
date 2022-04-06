#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
__file__    =  'worker.py'
__author__  =  'king'
__time__    =  '2022/03/28 15:52:27'
__version__ =  '1.0'
'''

from kombu import Queue
from kombu.mixins import ConsumerMixin
from kombu import Connection


queue = Queue('task_queue', routing_key='task_queue')


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
