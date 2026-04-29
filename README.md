TASK-1
The Classic File Transfer (Real-Time File Transfer and Verification)

Simple File Transfer with Checksum Verification

This is a basic client-server file transfer system built using Python sockets and pickle library for serialization. 
The goal is to send a file, break it into chunks on the server, and verify integrity using a checksum.

How it works:
The client sends a file to the server

The server:
Receives the file
Computes a SHA-256 checksum
Splits the file into 1024-byte chunks
Shuffles chunks to simulate out-of-order delivery
The client:
Receives all chunks
Reconstructs the file in the correct order
Verifies integrity using the checksum

How to run:
Start the server: python server.py

Run the client: python client.py
Make sure to update the file path in client.py before running.

Notes:
Uses TCP sockets (socket module)
File is split into fixed-size chunks (1024 bytes)
Chunks are sent in random order
Sequence numbers are used to reorder data correctly
SHA-256 checksum ensures file integrity

TASK-2

The Multi-Client Mayhem (Real-Time Multi-Client File Transfer and Verification):
This project implements a simple file transfer system using Python asyncio. It simulates an unreliable network where chunks can be dropped or corrupted, and handles recovery using retransmission and checksum verification.

How it works
The client sends a file to the server
The server splits it into 1024-byte chunks
Some chunks are randomly dropped or corrupted
The client detects missing chunks and requests them again
The server retransmits only the missing ones
A SHA-256 checksum is used to verify final file integrity

How to run:
start the server in a terminal: python server.py
run the client in separate terminals: python client.py sample.txt

Notes:
Up to 2 chunks may be dropped intentionally
Some chunks may be corrupted based on probability
The client reconstructs the file in correct order using sequence numbers
Final checksum comparison ensures correctness
