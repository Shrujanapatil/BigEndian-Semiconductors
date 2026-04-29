import asyncio
import hashlib
import random

HOST='127.0.0.1'
PORT=5001
corrupt_prob=0.2

def corrupt(chunk):
    if len(chunk)==0:
        return chunk
    i=random.randint(0,len(chunk)-1)
    return chunk[:i]+b"X"+chunk[i+1:]

def split_file(data):
    return [(i//1024,data[i:i+1024]) for i in range(0,len(data),1024)]

def checksum_calculated(data):
    checksum=hashlib.sha256(data).hexdigest()
    return checksum

async def handle_client(reader,writer):
    size_data=await reader.read(16)
    file_size=int(size_data.decode())
    data=b""
    while len(data)<file_size:
        data+=await reader.read(1024)
    print("File Received")

    chunks=split_file(data)
    checksum=checksum_calculated(data)

    original_chunks = {seq: chunk for seq, chunk in chunks}

    random.shuffle(chunks)
    num_to_drop = random.randint(0, min(2, len(chunks)))
    drop_indices = set(random.sample(range(len(chunks)), num_to_drop))
    sent_chunks = []
    for i, (org_seq, chunk) in enumerate(chunks):
        if i in drop_indices:
            print(f"Dropping chunk {org_seq}")
            continue
        
        if random.random() < corrupt_prob:
            print(f"Corrupting chunk {org_seq}")
            chunk = corrupt(chunk)

        sent_chunks.append((org_seq, chunk))

    writer.write(str(len(sent_chunks)).encode().ljust(16))
    await writer.drain()

    for org_seq, chunk in sent_chunks:
        header=f"{org_seq}".encode().ljust(16) + str(len(chunk)).encode().ljust(16)
        writer.write(header + chunk)
        await writer.drain()
    # Wait for missing chunk request

    missing_data = await reader.read(256)
    missing_list = eval(missing_data.decode().strip())
    for seq in missing_list:
        print("Retransmitting chunk", seq)
        chunk = original_chunks[seq]
        header = f"{seq}".encode().ljust(16) + str(len(chunk)).encode().ljust(16)
        writer.write(header + chunk)
        await writer.drain()
    writer.write(checksum.encode())
    await writer.drain()

    writer.close()


async def main():
    server=await asyncio.start_server(handle_client,HOST,PORT)
    print(f"Server is listening on {HOST} and {PORT}")
    async with server:
        await server.serve_forever()
    
if __name__=="__main__":
    asyncio.run(main())