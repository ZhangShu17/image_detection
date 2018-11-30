# -*- coding: utf-8 -*-
import socket
import time
import requests
import json

host = '0.0.0.0'
port = 8080


def reset_database():
    url = 'http://127.0.0.1:8000/autodrive/reset/'
    r = requests.post(url=url)
    json_data = json.loads(r.text)
    print(json_data)
    return json_data['retCode']


if __name__ == "__main__":
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = (host, port)
    serverSocket.bind(host)
    # serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.listen(2)
    serverSocket.setblocking(False)
    serverSocket.settimeout(2.0)
    print("server running")
    while True:
        try:
            clientSocket, addressInfo = serverSocket.accept()
            print("get connected")
            clientSocket.send(bytes('connect', encoding='utf-8'))
            receivedData = str(clientSocket.recv(2048))
            print(receivedData)
        except Exception as ex:
            print(Exception, ':', ex)
            result = reset_database()
            print('result={}'.format(result))
        time.sleep(1.5)
