#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
__file__    =  'receive_logs_topic.py'
__author__  =  'king'
__time__    =  '2022/03/31 11:25:15'
__version__ =  '1.0'
"""

from kombu import Queue
from kombu import Connection
from kombu.mixins import ConsumerProducerMixin


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


class Worker(ConsumerProducerMixin):
    def __init__(self, connection) -> None:
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=[Queue('rpc_queue')],
                accept={'text/plain', 'application/json'},
                on_message=self.on_request,
                prefetch_count=1,
            ),
        ]

    def on_request(self, message):
        n = message.payload.get('n')
        print(f' [.] fib({n})')
        result = fib(n)
        self.producer.publish(
            {'result': result},
            exchange='',
            routing_key=message.properties['reply_to'],
            correlation_id=message.properties['correlation_id'],
            serializer='json',
            retry=True,
        )
        message.ack()


with Connection('amqp://guest:guest@localhost:5672//') as connection:
    try:
        worker = Worker(connection=connection)
        worker.run()
    except KeyboardInterrupt:
        print('bye bye')
