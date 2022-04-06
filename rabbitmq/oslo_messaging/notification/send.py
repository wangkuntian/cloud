# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__project__ =  'cloud'
__file__    =  'send.py'
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

transport_url = "rabbit://guest:guest@127.0.0.1:5672/"

transport = messaging.get_notification_transport(cfg.CONF, transport_url)

notifier = messaging.Notifier(
    transport,
    publisher_id="local",
    driver="messaging",
    topics=["notifications"],
)

client = notifier.prepare()
client.info({}, event_type="my_type", payload={"content": "Hello World"})
client.error({}, event_type="error_type", payload={"content": "Hello World"})
