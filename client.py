import socket
import threading
import sys

server = (sys.argv[1],int(sys.argv[2]))
p1 = '50001' #port you use to talk to the server
p2 = '50002' #port you use to create peer connection

def bootstrap():
    print("Connecting to bootstrap server...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', int(p1)))
    sock.sendto(p2.encode(),server)
    print("Waiting for server....")
    while True:
        data = sock.recv(1024).decode()
        if data.strip() == "ready":
            print("Connected to server successfully")
            break
    data = sock.recv(1024).decode().split()
    ip,port = data
    punch_hole(ip,int(port))

def punch_hole(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', int(p2)))
    sock.sendto(b'0',(ip,port))
    print("Punching hole")
    listener = threading.Thread(target=listen, args=(sock,), daemon=True);
    listener.start()
    while True:
        msg = input()
        sock.sendto(msg.encode(),(ip,port))

def listen(sock):
    while True:
        data = sock.recv(1024).decode()

        print("\npeer:{}\n".format(data))
bootstrap()