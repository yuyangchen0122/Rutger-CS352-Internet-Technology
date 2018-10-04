import numpy as mypy
import threading
import time
import random
import socket as mysoc


def reverse(a_string):
    t = a_string.rstrip()
    return t[::-1] + "\n"


def server():
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', 50010)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at", addr)

    while 1:
        with open('PROJI-DNSRS.txt') as f:
            lines = f.readlines()
        f.close()
        data_from_client = csockid.recv(1024)
        m = data_from_client.decode('utf-8')
        if not data_from_client:
            break
        print("[C]: Data received from server:", m)
        for line in lines:
            time.sleep(1)
            if line.startswith('m'):
                print(line)

    # Close the server socket
    ss.close()
    exit()


t1 = threading.Thread(name='server', target=server)
t1.start()

input("Hit ENTER  to exit")

exit()