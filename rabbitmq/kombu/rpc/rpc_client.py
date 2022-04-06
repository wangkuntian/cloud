#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""

__file__    =  'emit_log_topic.py'
__author__  =  'king'
__time__    =  '2022/03/31 11:15:12'
__version__ =  '1.0'
"""

from kombu import uuid
from kombu import Queue
from kombu import Consumer
from kombu import Connection
from kombu import producers


class FibonacciRpcClient(object):
    def __init__(self):
        self.response = None
        self.correlation_id = None
        self.connection = Connection("amqp://guest:guest@localhost:5672//")
        self.queue = Queue("rpc_queue", routing_key="rpc_queue")

    def call(self, n: object):
        self.correlation_id = uuid()
        with producers[self.connection].acquire(block=True) as producer:
            producer.publish(
                body={"n": n},
                routing_key="rpc_queue",
                queue=self.queue,
                declare=[self.queue],
                reply_to=self.queue.name,
                correlation_id=self.correlation_id,
            )
        with Consumer(
            self.connection,
            on_message=self.on_response,
            queues=[self.queue],
            no_ack=True,
        ):
            while self.response is None:
                self.connection.drain_events()

        return self.response

    def on_response(self, message):
        if message.properties["correlation_id"] == self.correlation_id:
            self.response = message.payload.get("result")


client = FibonacciRpcClient()
print(" [x] Requesting fib(30)")
result = client.call(30)
print(f" [✔️] Got {result!r}")
