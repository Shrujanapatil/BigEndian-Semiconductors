import asyncio
import hashlib
import sys

HOST='127.0.0.1'
PORT=5001
def checksum_calculated(data):
    checksum=hashlib.sha256(data).hexdigest()
    return checksum

async def send_and_receive(file_path):
    reader,writer=await asyncio.open_connection(HOST,PORT)
    with open(file_path,'rb') as f:
        data=f.read()
    writer.write(str(len(data)).encode().ljust(16))#pad it to 16 bytes
    await writer.drain()

    writer.write(data)
    await writer.drain()

    num_chunks=int((await reader.read(16)).decode())
    chunks=[]
    for _ in range(num_chunks):
        seq_header=await reader.read(16)
        size_header=await reader.read(16)
        seq=int(seq_header.decode())
        chunk_size=int(size_header.decode())
        chunk=await reader.read(chunk_size)
        chunks.append((seq,chunk))
    
    # Detect missing chunks
    received_seq = set(seq for seq, _ in chunks)
    expected_seq = set(range(num_chunks))

    missing = expected_seq - received_seq

    # Send missing sequence numbers to server
    writer.write(str(list(missing)).encode().ljust(256))
    await writer.drain()

    # Receive retransmitted chunks
    for _ in range(len(missing)):
        seq_header = await reader.read(16)
        size_header = await reader.read(16)

        seq = int(seq_header.decode())
        chunk_size = int(size_header.decode())

        chunk = await reader.read(chunk_size)
        chunks.append((seq, chunk))

    received_checksum=(await reader.read(64)).decode()

    reconstructed_data=b""
    for seq,chunk in sorted(chunks):
        reconstructed_data+=chunk
    calculated_checksum=checksum_calculated(reconstructed_data)

    if calculated_checksum==received_checksum:
        print("File received successfully with correct checksum.") 
    else:
        print("Checksum mismatch! File may be corrupted.")

    writer.close()
    

     
if __name__=="__main__":
    file_path=sys.argv[1]
    asyncio.run(send_and_receive(file_path))