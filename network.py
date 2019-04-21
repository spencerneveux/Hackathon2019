# Echo client program
import socket
import threading

HOST = '127.0.0.1'    # The remote host
PORT = 10002              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
	    message = input("Enter: ")
	    s.sendall(message.encode('utf-8'))
	    data = s.recv(1024)
	    if not data: break
    print(repr(data))
    
    
# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 10002              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print('Listening')
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data: 
        	print("Disconnected By: " + str(addr[0]))
        	break
        conn.sendall(data)
