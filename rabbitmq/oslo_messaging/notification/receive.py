# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__project__ =  'cloud'
__file__    =  'receive.py'
__author__  =  'king'
__time__    =  '2022/4/6 15:10'


                              _ooOoo_
                             o8888888o
                             88" . "88
                             (| -_- |)
                             O\  =  /O
                          ____/`---'\____
                        .'  \\|     |//  `.
                       /  \\|||  :  |||//  \
                      /  _||||| -:- |||||-  \
                      |   | \\\  -  /// |   |
                      | \_|  ''\---/''  |   |
                      \  .-\__  `-`  ___/-. /
                    ___`. .'  /--.--\  `. . __
                 ."" '<  `.___\_<|>_/___.'  >'"".
                | | :  `- \`.;`\ _ /`;.`/ - ` : | |
                \  \ `-.   \_ __\ /__ _/   .-` /  /
           ======`-.____`-.___\_____/___.-`____.-'======
                              `=---='
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                       佛祖保佑        永无BUG
"""

from oslo_config import cfg
import oslo_messaging as messaging


class NotificationEndpoint(object):
    filter_rule = messaging.NotificationFilter(publisher_id="^local.*")

    def info(self, context, publish_id, event_type, payload, metadata):
        print("Info")
        print(context, publish_id, event_type, payload, metadata)

    def warn(self, context, publish_id, event_type, payload, metadata):
        print("Warn")
        print(context, publish_id, event_type, payload, metadata)

    def error(self, context, publish_id, event_type, payload, metadata):
        print("Error")
        print(context, publish_id, event_type, payload, metadata)


transport_url = "rabbit://guest:guest@127.0.0.1:5672/"

transport = messaging.get_notification_transport(cfg.CONF, transport_url)
target = messaging.Target(topic="notifications")
listener = messaging.get_notification_listener(
    transport,
    targets=[target],
    endpoints=[NotificationEndpoint()],
    pool='listener'
)
listener.start()
listener.wait()
