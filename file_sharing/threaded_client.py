import socket
import threading



from protocol import parse_message

HOST = input("Enter host IP: ")
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

                try:
                    message_type, content = parse_message(message)
                except ValueError as error:
                    print(f"\nInvalid message: {error}")
                    continue
                if message_type == "CHAT" and content == "/quit":
                    print("\nFriend ended the chat.")
                    return

                if message_type == "CHAT":
                    print(f"\nFriend: {content}")
                else:
                    print(f"\nUnknown message type: {message_type}")


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
        client.sendall(("CHAT|" + message + "\n").encode())

        if message == "/quit":
            break
finally:
    client.close()
    print("Chat closed.")
