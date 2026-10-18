
import os
import struct


def send_file(sock, file_path):
    file_size = os.path.getsize(file_path)

    # Send the file size as an unsigned 64-bit integer.
    sock.sendall(struct.pack("!Q", file_size))

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

            sock.sendall(chunk)


def receive_file(sock, destination):
    # Read the 8-byte file size header.
    header = receive_exact(sock, 8)
    file_size = struct.unpack("!Q", header)[0]

    received = 0

    with open(destination, "wb") as file:
        while received < file_size:
            chunk_size = min(4096, file_size - received)
            chunk = receive_exact(sock, chunk_size)
            file.write(chunk)
            received += len(chunk)

    print(f"Received {received} bytes into {destination}")
