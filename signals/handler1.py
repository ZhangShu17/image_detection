# -*- coding: utf-8 -*-
from monitor.models import PersonFace, Transaction, Obstacle
from direction.models import Command, ControlState, StopStatus
from django.db.models import signals
from django.dispatch import receiver
import socket
from constants import constants
import time
import logging

# logger = logging.getLogger(__name__)
#
#
# @receiver(signals.post_save, sender=Command)
# def create_command(sender, instance, created, **kwargs):
#     if created:
#         print('command created!')
#         return 'Command'
#
#
# @receiver(signals.post_save, sender=Transaction)
# def create_transaction(sender, instance, created, **kwargs):
#     if created:
#         print('transaction created!')
#         serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         host = ("127.0.0.1", 8080)
#         serverSocket.bind(host)
#         serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         serverSocket.listen(1)
#         serverSocket.setblocking(False)
#         serverSocket.settimeout(100)
#         try:
#             clientSocket, addressInfo = serverSocket.accept()
#         except Exception as ex:
#             logger.error(ex)
#             serverSocket.close()
#         print("server running")
#         while True:
#             try:
#                 print("get connected")
#                 data = {
#                     'type': 0,
#                     'value': 10
#                 }
#                 clientSocket.send(bytes(data))
#                 print('time={}'.format(time.time()))
#                 receivedData = str(clientSocket.recv(2048))
#                 print(receivedData)
#                 if receivedData:
#                     serverSocket.close()
#                     break
#             except Exception as ex:
#                 logger.error(ex)
#                 serverSocket.close()
#                 break
#
#
# @receiver(signals.post_save, sender=Obstacle)
# def create_obstacle(sender, instance, created, **kwargs):
#     if created:
#         print('obstacle created!')
#         return 'Obstacle'


