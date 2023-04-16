import socket

# Define host and port
host = "127.0.0.1"
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
msg = "Hello from client 1"
s.send(msg.encode())
s.close()
