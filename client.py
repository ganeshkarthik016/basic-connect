
import socket

HOST = "enter ur friend ip address here"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))
print("Connected to host! Type /quit to exit.")

try:
    while True:
        message = input("You: ")
        client.sendall(message.encode())

        if message == "/quit":
            break

        data = client.recv(1024)

        if not data:
            print("Host disconnected.")
            break

        reply = data.decode()
        print(f"Host: {reply}")

        if reply == "/quit":
            break

finally:
    client.close()
    print("Disconnected.")
