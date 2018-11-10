# Yuyang Chen  168008482 yc791
# Yuezhong Yan yy378

import threading
import time
import random
import socket as mysoc


class count:
    counter = 0
    ctoTLDS1 = None
    ctoTLDS2 = None


def reverse(a_string):
    t = a_string.rstrip()
    return t[::-1] + "\n"


def connect_to_tlds1():
    try:
        tlds1 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        count.ctoTS = tlds1
        print("[C]: Connect to TLDS1")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    port_tlds1 = 50000
    sa_sameas_myaddr = mysoc.gethostbyname()
    server_binding1 = (sa_sameas_myaddr, port_tlds1)
    tlds1.connect(server_binding1)
    return tlds1


def connect_to_tlds2():
    try:
        tlds2 = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        count.ctoTLDS2 = tlds2
        print("[C]: Connect to TLDS2")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    port_tlds2 = 50001
    sa_sameas_myaddr = mysoc.gethostbyname()
    server_binding2 = (sa_sameas_myaddr, port_tlds2)
    tlds2.connect(server_binding2)
    return tlds2


def server():
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', 50021)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at", addr)
    tssd1, addr1 = ss.accept()
    print("[S]: Got a connection request from a TLDS1 at", addr1)
    tssd2, addr2 = ss.accept()
    print("[S]: Got a connection request from a TLDS2 at", addr2)

    while 1:
        with open('PROJ2-DNSRS.txt') as f:
            lines = f.readlines()
        f.close()
        data_from_client = csockid.recv(1024)
        m = data_from_client.decode('utf-8')
        if not data_from_client:
            break
        print("[C]: Data received from client:", m)
        time.sleep(1)
        temp = 0
        for line in lines:
            if line.startswith(m):
                print("Hostname IPaddress A: ", line)
                csockid.send(line.encode('utf-8'))
                time.sleep(1)
                temp = 1
                break

        if temp == 0:
            if m.endswith(".edu"):
                print("TSHostname .EDU: ", m)
                temp1 = line.strip("\n") + "\n"
                csockid.send(temp1.encode('utf-8'))
                time.sleep(1)
            if m.endswith(".com"):
                print("TSHostname .COM: ", m)
                temp2 = line.strip("\n") + "\n"
                csockid.send(temp2.encode('utf-8'))
                time.sleep(1)
            else:
                csockid.send("Error".encode('ufg-8'))

        data_from_server1 = tssd1.recv(1024)
        s1 = data_from_server1.decode('uft-8')
        if not data_from_server1:
            break
        print("[C]: Data received from TLDS1:", s1)
        csockid.send(s1.encode('utf-8'))
        time.sleep(1)

        data_from_server2 = tssd2.recv(1024)
        s2 = data_from_server2.decode('uft-8')
        if not data_from_server2:
            break
        print("[C]: Data received from TLDS2:", s2)
        csockid.send(s2.encode('utf-8'))
        time.sleep(1)

    # Close the server socket
    ss.close()
    exit()


t1 = threading.Thread(name='server', target=server)
t1.start()

input("Hit ENTER  to exit")

exit()