#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

while True:
    print("Client starting - Connecting to server at IP", HOST, "and port", PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connection established.")
        print("Enter request (translate <word> or learn <lesson_number> (lesson_number: integer from 1 to 10)):")
        command = input().lower()
        s.sendall(bytes(command, 'utf-8'))
        print("Message sent, waiting for reply.")
        response = s.recv(1024).decode()

    print(f"Received response: {response}".replace('\\n', '\n'))
    
    # Check if the request is successfully finished
    if response not in ["Unknown command. Try again.", "Translation not found. Try again.", "Lesson not found. Try again."]:
        break

print("Client is done!")