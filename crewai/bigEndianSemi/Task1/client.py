import socket
import pickle
import hashlib


HOST='127.0.0.1'
PORT=5001

def calculate_checksum(file_data):

    sha256 = hashlib.sha256()
    sha256.update(file_data)
    return sha256.hexdigest()

def send_data(file_path):
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))

    with open(file_path,'rb') as f:
        file_data=f.read()

    client_socket.sendall(file_data)

    client_socket.shutdown(socket.SHUT_WR)
    print("File successfully sent to server")

    num_chunks= pickle.loads(client_socket.recv(4096))

    received_checksum=pickle.loads(client_socket.recv(4096))

    print(f"Received checksum: {received_checksum} \n")

    received_chunks={}
    for _ in range(num_chunks):
        sequence_number,chunk_data=pickle.loads(client_socket.recv(4096))
        received_chunks[sequence_number]=chunk_data
    
    if len(received_chunks)==num_chunks:
        print("All chunks received : ")

        reconstructed_file=b""
        for i in range(num_chunks):
            reconstructed_file+=received_chunks[i]

        calculated_checksum=calculate_checksum(reconstructed_file)
        if calculated_checksum==received_checksum:
            print("File integrity verified successfully. Checksums match.")
        else:
            print("File integrity verification failed. Checksums do not match.")
            client_socket.close()
            

    else:
        client_socket.close()
       

if __name__=="__main__":
    file_path=r"C:\Users\prady\projects\crew_ai\crewai\bigEndianSemi\test.txt"
    send_data(file_path)