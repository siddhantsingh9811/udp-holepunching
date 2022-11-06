import socket
import sys

server_port = int(sys.argv[1])

# create datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(('0.0.0.0',server_port))

clients = []
def exchange_info(c1,c2):
    #send shit to c1
    sock.sendto("{} {}".format(c2[0][0],c2[1]).encode(),c1[0])

    sock.sendto("{} {}".format(c1[0][0],c1[1]).encode(),c2[0])

    print("Hole Punched")
while True:
    data, address = sock.recvfrom(1024)
    print("Connection from {}, requesting poert {}".format(address,data))
    sock.sendto(b'ready',address)
    
    clients.append([address,data.decode()])
    if len(clients) == 2:
        c1 = clients.pop()
        c2 = clients.pop()
        exchange_info(c1,c2)
        break
