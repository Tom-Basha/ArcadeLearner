import socket

# Define host and port
host = "127.0.0.1"
port = 12345

def run_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(2)

    print("Waiting for client connections...")

    # Wait for two clients to connect
    trainer, client1_address = server_socket.accept()
    print(f"Connection established with Trainer: {client1_address}")
    game, client2_address = server_socket.accept()
    print(f"Connection established with Game: {client2_address}")

    # Receive message from Trainer
    requested_attributes = trainer.recv(1024).decode()
    print(f"Received message from Trainer: {requested_attributes}")

    # Send message to Game
    if requested_attributes:
        game.send(requested_attributes.encode())
        print(f"Trainer => Game: {requested_attributes}")

    # Receive messages from Game
    while True:
        try:
            data = game.recv(1024)
            if not data:
                break
            trainer.send(data)
            print(f"Game => Trainer: {data.decode()}")

        except:
            break

    # Close the connections
    trainer.close()
    game.close()
    server_socket.close()

    # Restart server to listen for new clients
    run_server()

if __name__ == "__main__":
    run_server()
