FTP Using Socket Programming
A simple File Transfer Protocol (FTP) application developed in Python using Socket Programming. This project demonstrates how a client and server can communicate over a TCP connection to upload, download, and list files using a custom message-framing protocol.

Features
•	TCP socket-based client-server communication
•	List files stored on the server
•	Upload files from client to server
•	Download files from server to client
•	Custom message framing using a 4-byte length header

Technologies Used
•	Python 3
•	Socket Programming
•	TCP/IP
•	socket module
Project Structure

FTP-Using-Socket-Programming/
│
├── ftp_client.py
├── ftp_server.py
├── server_storage/
│        └── uploaded files
│
└── README.md

The server_storage directory is automatically created when the server starts if it does not already exist.
Communication Process
1.	The server creates a TCP socket.
2.	The server binds to 127.0.0.1:65432.
3.	The server listens for incoming client connections.
4.	The client connects to the server.
5.	The client sends commands such as LIST, UPLOAD, or DOWNLOAD.
6.	The server processes the requested operation.
7.	The server sends a response back to the client.
8.	The connection remains active until the client sends EXIT.

Message Framing
TCP is a stream-oriented protocol, so a single recv() call does not necessarily return an entire message. To solve this problem, this project uses a 4-byte big-endian length header before every message.
┌──────────────────┬──────────────────────────────┐
│ 4-byte Length    │ Message Payload              │
└──────────────────┴──────────────────────────────┘
For example:
Length → 00000004
Data   → LIST
The send_msg() function adds the length header:
sock.sendall(struct.pack(">I", len(msg_bytes)) + msg_bytes)
The recv_msg() function first receives the 4-byte length and then receives exactly that number of bytes.

This ensures that complete messages and file data can be transferred reliably.
Getting Started
1. Clone the Repository
git clone https://github.com/afroza054/client.py.git
2. Navigate to the Project Directory
Cd client.py
3. Check Python Installation
Make sure Python 3 is installed:
python --version
or:
python3 --version
No external Python packages are required.

Running the Project
Step 1: Start the Server
Open a terminal and run:
python ftp_server.py
You should see:
FTP Server listening on 127.0.0.1:65432
Step 2: Start the Client
Open another terminal in the same project directory:
python ftp_client.py
You should see:
Connected to FTP server at 127.0.0.1:65432

Available Commands: LIST, UPLOAD <filename>, DOWNLOAD <filename>, EXIT
You can now enter FTP commands.
Available Commands
Command	Description

LIST	Displays files available on the server
UPLOAD <filename>	Uploads a local file to the server
DOWNLOAD <filename>	Downloads a file from the server

EXIT	Closes the client connection

1. LIST
To see the files stored on the server:
ftp> LIST
Example output:
document.txt
photo.jpg
example.pdf
If there are no files:
Storage is empty.

2. UPLOAD
To upload a file:
ftp> UPLOAD document.txt
The client reads the file and sends its contents to the server.
The server stores the file inside:
server_storage/
Example:
SUCCESS: File uploaded.
  │                               │
3. DOWNLOAD
To download a file:
ftp> DOWNLOAD document.txt
The server checks whether the requested file exists.
If the file exists:
SUCCESS: File downloaded as 'downloaded_document.txt'
The downloaded file is saved in the client's current directory with the prefix:
downloaded_
For example:
hello.txt
becomes:
downloaded_hello.txt

4. EXIT
To terminate the FTP session:
ftp> EXIT
The client sends the EXIT command and closes the connection.
Error Handling
The application handles several common errors, including:
•	Server connection failure
•	Local file not found during upload
•	Requested server file not found during download
•	Invalid or malformed commands
•	File reading/writing errors
•	Unexpected socket disconnection
Example:
ftp> UPLOAD unknown.txt

Local file 'unknown.txt' does not exist.
Important Functions
send_msg()
Adds a 4-byte message length header before sending data.
def send_msg(sock, msg_bytes):
    sock.sendall(
        struct.pack(">I", len(msg_bytes)) + msg_bytes
    )
recv_msg()
Receives the message length and then retrieves the complete message.
def recv_msg(sock):
    raw_msglen = recvall(sock, 4)

    if not raw_msglen:
        return None

    msglen = struct.unpack(">I", raw_msglen)[0]

    return recvall(sock, msglen)
recvall()
Ensures that exactly the required number of bytes are received.
def recvall(sock, n):
    data = bytearray()

    while len(data) < n:
        packet = sock.recv(n - len(data))

        if not packet:
            return None

        data.extend(packet)

    return bytes(data)

Example Session
Server
FTP Server listening on 127.0.0.1:65432
Connection accepted from ('127.0.0.1', 54321)
Client
Connected to FTP server at 127.0.0.1:65432

Available Commands: LIST, UPLOAD <filename>, DOWNLOAD <filename>, EXIT

ftp> LIST
Storage is empty.

ftp> UPLOAD test.txt
SUCCESS: File uploaded.

ftp> LIST
test.txt

ftp> DOWNLOAD test.txt
SUCCESS: File downloaded as 'downloaded_test.txt'

ftp> EXIT
Disconnected from server.
Limitations
This project is designed for educational purposes and demonstrates the fundamentals of socket-based file transfer.
Current limitations include:
•	Uses 127.0.0.1, so it is intended primarily for local testing.
•	No user authentication.
•	No encryption.
•	Files are transferred into memory before being written to disk.
•	The server handles clients sequentially rather than using threads.
•	No advanced FTP features such as directories, file permissions, or resume support.
•	File paths should be handled carefully before using this implementation in a production environment.
Future Improvements
Possible improvements include:
•	Multi-client support using threading
•	Username/password authentication
•	TLS/SSL encryption
•	File transfer progress indicators
•	Directory creation and navigation
•	File deletion and renaming
•	Resume interrupted downloads
•	Logging system
•	Graphical User Interface (GUI)

Learning Objectives
This project helps demonstrate:
•	Client-server architecture
•	TCP socket programming
•	Network communication
•	Message framing
•	Sending and receiving binary data
•	File I/O in Python
•	Exception handling
•	Basic FTP concepts


Author
Afroza Jabin Ruma
GitHub: https://github.com/afroza054

