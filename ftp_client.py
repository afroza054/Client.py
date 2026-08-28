import os
import socket
import struct

HOST = "127.0.0.1"
PORT = 65432


def send_msg(sock, msg_bytes):
    sock.sendall(struct.pack(">I", len(msg_bytes)) + msg_bytes)


def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack(">I", raw_msglen)[0]
    return recvall(sock, msglen)


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return bytes(data)


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"[+] Connected to FTP server at {HOST}:{PORT}")
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return

    print("\nAvailable Commands: LIST, UPLOAD <filename>, DOWNLOAD <filename>, EXIT")

    while True:
        user_input = input("\nftp> ").strip()
        if not user_input:
            continue

        parts = user_input.split(" ", 1)
        cmd = parts[0].upper()

        if cmd == "EXIT":
            send_msg(client_socket, b"EXIT")
            break

        elif cmd == "LIST":
            send_msg(client_socket, b"LIST")
            response = recv_msg(client_socket)
            print(response.decode("utf-8"))

        elif cmd == "UPLOAD":
            if len(parts) < 2:
                print("Usage: UPLOAD <filename>")
                continue
            filename = parts[1]

            if not os.path.exists(filename):
                print(f"Local file '{filename}' does not exist.")
                continue

            # Send command metadata
            send_msg(client_socket, f"UPLOAD {filename}".encode("utf-8"))

            # Read and send file bytes
            with open(filename, "rb") as f:
                file_bytes = f.read()
            send_msg(client_socket, file_bytes)

            # Get server confirmation
            response = recv_msg(client_socket)
            print(response.decode("utf-8"))

        elif cmd == "DOWNLOAD":
            if len(parts) < 2:
                print("Usage: DOWNLOAD <filename>")
                continue
            filename = parts[1]

            # Send command metadata
            send_msg(client_socket, f"DOWNLOAD {filename}".encode("utf-8"))

            # Check if server is ready/has the file
            status = recv_msg(client_socket).decode("utf-8")
            if status.startswith("ERROR"):
                print(status)
                continue

            # Receive the raw file bytes
            file_bytes = recv_msg(client_socket)
            with open(f"downloaded_{filename}", "wb") as f:
                f.write(file_bytes)
            print(f"SUCCESS: File downloaded as 'downloaded_{filename}'")

        else:
            print("Unknown command.")

    client_socket.close()
    print("[-] Disconnected from server.")


if __name__ == "__main__":
    run_client()