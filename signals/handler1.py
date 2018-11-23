# -*- coding: utf-8 -*-
from monitor.models import PersonFace
from django.db.models import signals
from django.dispatch import receiver
import socket
from constants import constants


# @receiver(signals.post_save, sender=PersonFace)
# def create_person_face(sender, instance, created, **kwargs):
#     if created:
#         print('created!')
#         sk = socket.socket()
#         sk.bind((constants.socket_host, constants.socker_port))
#         sk.listen(5)
#         conn, address = sk.accept()
#         print('conn={},address={}'.format(conn, address))
#         conn.sendall(bytes('Face'))
#         call_back = conn.recv(1024)
#         if call_back:
#             print(call_back)
#             print('I have get call back from client')
#         sk.close()
#
#         # while True:
#         #     conn, address = sk.accept()
#         #     print('conn={},address={}'.format(conn, address))
#         #     conn.sendall(bytes('Face'))
#         #     call_back = conn.recv(1024)
#         #     if call_back:
#         #         print(call_back)
#         #         print('I have get call back from client')
#         #         sk.close()
#         #         break
