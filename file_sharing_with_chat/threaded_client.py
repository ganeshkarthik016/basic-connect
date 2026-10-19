
import socket
import threading

from protocol import CHAT, send_packet, receive_packet

HOST = input("Enter host IP: ")
PORT = 5000


def receive_messages(sock):
    try:
        while True:
            packet_type, payload = receive_packet(sock)

            if packet_type == CHAT:
                message = payload.decode("utf-8")
                print(f"\nFriend: {message}")
            else:
                print(f"\nUnknown packet type: {packet_type}")

    except (ConnectionError, OSError):
        print("\nHost disconnected.")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected! Type /quit to exit.")

thread = threading.Thread(
    target=receive_messages,
    args=(client,),
    daemon=True
)
thread.start()

try:
    while True:
        message = input("You: ")

        if message == "/quit":
            break

        send_packet(client, CHAT, message.encode("utf-8"))

finally:
    client.close()
    print("Chat closed.")
