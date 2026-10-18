
import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

def receive_messages(sock):
    buffer = b""

    while True:
        try:
            data = sock.recv(1024)

            if not data:
                print("\nFriend disconnected.")
                break

            buffer += data

            while b"\n" in buffer:
                raw_message, buffer = buffer.split(b"\n", 1)
                message = raw_message.decode()

                if message == "/quit":
                    print("\nFriend ended the chat.")
                    return

                print(f"\nFriend: {message}")

        except OSError:
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for a connection...")
conn, addr = server.accept()
print(f"Connected to {addr}")

thread = threading.Thread(target=receive_messages, args=(conn,))
thread.start()

try:
    while True:
        message = input("You: ")
        conn.sendall((message + "\n").encode())

        if message == "/quit":
            break
finally:
    conn.close()
    server.close()
    print("Chat closed.")
