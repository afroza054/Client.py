import os
import socket
import struct

# Configuration
HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 4096
STORAGE_DIR = "./server_storage"

# Ensure server storage directory exists
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)


def send_msg(sock, msg_bytes):
    """Prefixes each message with a 4-byte big-endian length header."""
    sock.sendall(struct.pack(">I", len(msg_bytes)) + msg_bytes)


def recv_msg(sock):
    """Reads the 4-byte length header to safely receive the full message payload."""
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack(">I", raw_msglen)[0]
    return recvall(sock, msglen)


def recvall(sock, n):
    """Helper function to receive exactly n bytes or return None if EOF."""
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return bytes(data)


def handle_list(conn):
    """Lists files in the storage directory."""
    try:
        files = os.listdir(STORAGE_DIR)
        files_str = "\n".join(files) if files else "Storage is empty."
        send_msg(conn, files_str.encode("utf-8"))
    except Exception as e:
        send_msg(conn, f"ERROR: {str(e)}".encode("utf-8"))


def handle_upload(conn, filename):
    """Receives file bytes from client and writes them to disk."""
    try:
        file_path = os.path.join(STORAGE_DIR, filename)
        # Receive the file content payload
        file_bytes = recv_msg(conn)
        if file_bytes is None:
            return

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        send_msg(conn, b"SUCCESS: File uploaded.")
    except Exception as e:
        send_msg(conn, f"ERROR: {str(e)}".encode("utf-8"))


def handle_download(conn, filename):
    """Reads file bytes from disk and sends them to the client."""
    file_path = os.path.join(STORAGE_DIR, filename)
    if not os.path.exists(file_path):
        send_msg(conn, b"ERROR: File not found.")
        return

    try:
        # First signal that the file exists
        send_msg(conn, b"READY")
        # Read and send the raw file bytes
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        send_msg(conn, file_bytes)
    except Exception as e:
        send_msg(conn, f"ERROR: {str(e)}".encode("utf-8"))


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[*] FTP Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        print(f"[+] Connection accepted from {addr}")

        while True:
            data = recv_msg(conn)
            if not data:
                print(f"[-] Connection closed by {addr}")
                break

            # Parse command string
            command_parts = data.decode("utf-8").split(" ", 1)
            cmd = command_parts[0].upper()

            if cmd == "LIST":
                handle_list(conn)
            elif cmd == "UPLOAD" and len(command_parts) > 1:
                handle_upload(conn, command_parts[1])
            elif cmd == "DOWNLOAD" and len(command_parts) > 1:
                handle_download(conn, command_parts[1])
            elif cmd == "EXIT":
                print(f"[-] Client {addr} requested exit.")
                break
            else:
                send_msg(conn, b"ERROR: Invalid or malformed command.")

        conn.close()


if __name__ == "__main__":
    start_server()