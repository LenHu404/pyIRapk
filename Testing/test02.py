import socket

def sendData():
    UDP_IP = "192.168.2.199"
    UDP_PORT = 5005
    MESSAGE = b"Test01 to IP"
    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % MESSAGE)
    sock = socket.socket(socket.AF_INET, # Internet
                          socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

sendData()