
import socket
import threading

from protocol import CHAT, send_packet, receive_packet

HOST = "0.0.0.0"
PORT = 5000


def receive_messages(conn):
    try:
        while True:
            packet_type, payload = receive_packet(conn)

            if packet_type == CHAT:
                message = payload.decode("utf-8")
                print(f"\nFriend: {message}")
            else:
                print(f"\nUnknown packet type: {packet_type}")

    except (ConnectionError, OSError):
        print("\nFriend disconnected.")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for a connection...")
conn, addr = server.accept()
print(f"Connected to {addr}")

thread = threading.Thread(
    target=receive_messages,
    args=(conn,),
    daemon=True
)
thread.start()

try:
    while True:
        message = input("You: ")

        if message == "/quit":
            break

        send_packet(conn, CHAT, message.encode("utf-8"))

finally:
    conn.close()
    server.close()
    print("Chat closed.")
