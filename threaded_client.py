
import socket
import threading

HOST = input("Enter host IP: ")
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)

            if not data:
                print("\nHost disconnected.")
                break

            print("\nFriend:", data.decode().rstrip("\n"))

        except OSError:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected! Type /quit to exit.")

thread = threading.Thread(target=receive_messages, args=(client,))
thread.start()

try:
    while True:
        message = input("You: ")
        client.sendall((message + "\n").encode())

        if message == "/quit":
            break
finally:
    client.close()
    print("Chat closed.")
