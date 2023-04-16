import socket

host = "127.0.0.1"
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
data = s.recv(1024).decode()
print(f"Received message from server: {data}")

while True:
    msg = "CLIENT 2"
    s.send(msg.encode())

# Close the connection
s.close()
