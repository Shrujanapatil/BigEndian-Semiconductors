import socket
import hashlib
import random
import pickle
HOST='127.0.0.1'
PORT=5001
CHUNK_SIZE=1024

def checksum_calc(file_data):
    checksum=hashlib.sha256(file_data)
    checksum=checksum.hexdigest()
    return checksum

def split_into_chunks(file_data):
    chunks_list=[]
    for i in range(0,len(file_data),CHUNK_SIZE):
        chunk_data=file_data[i:i+CHUNK_SIZE]
        sequence_number=i//CHUNK_SIZE
        chunks_list.append((sequence_number,chunk_data))
    return chunks_list

def start_server():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))

    server_socket.listen(1)
    print("The server is listening :")

    conn,addr=server_socket.accept()
    print(f"Client connection assigned to {addr}")

    file_data=b""

    while True:
        data=conn.recv(4096)
        if not data:
            break
        file_data+=data

    print("File received successfully from client")

    checksum=checksum_calc(file_data)
    print(f"Checksum : {checksum}")
    
    chunks=split_into_chunks(file_data)

    random.shuffle(chunks)#out of order delivery

    conn.send(pickle.dumps(len(chunks)))
    conn.send(pickle.dumps(checksum))
    numofchunks=len(chunks)

    for chunk in chunks:
        serialized_chunk=pickle.dumps(chunk)
        conn.send(serialized_chunk)

    print("Chunks sent to client. ")

    conn.close()
    server_socket.close()



if __name__=="__main__":
    start_server()
