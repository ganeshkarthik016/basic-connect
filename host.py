
import socket

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(1)

print(f"Listening on port {PORT}...")

conn, addr = server.accept()
print(f"Connected by {addr}")

try:
    while True:
        data = conn.recv(1024)

        if not data:
            print("Client disconnected.")
            break

        message = data.decode()
        print(f"Client: {message}")

        if message == "/quit":
            break

        reply = input("You: ")
        conn.sendall(reply.encode())

        if reply == "/quit":
            break

finally:
    conn.close()
    server.close()
    print("Connection closed.")
