import boto.sqs
from boto.sqs.message import Message
import os
import config

conn = boto.sqs.connect_to_region("us-west-2",
                                  aws_access_key_id=config.sqs_access_key,
                                  aws_secret_access_key=config.sqs_access_secret)

queue = conn.get_queue("Image")
queuepkg = conn.get_queue("Package")


while (True):
    messages = queue.get_messages()
    for mes in messages:
        dname = mes.get_body()
        print dname
        res = os.popen('./script.sh ' + dname)
        for i in range(4):
            res.readline()
        pkglist = res.read()
        mes = Message()
        mes.set_body(pkglist)
        queuepkg.write(mes)
    if (len(messages) != 0):
        queue.delete_message_batch(messages)
