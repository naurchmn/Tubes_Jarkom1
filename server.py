import socket
import threading
import queue
from rsa_module import generate_keys, encrypt, decrypt

messages = queue.Queue()
clients = []
PASSWORD = "12345"
auth_clients={}
usernames = set()
username_map = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 9999))
public_key, private_key = generate_keys() # generate key buat server
client_public_keys = {} #simpen public key client

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)

            if addr not in auth_clients:
                if addr not in client_public_keys:
                    # pesan pertama klien kunci publiknya klien
                    e, n = map(int, message.decode().split(","))
                    client_public_keys[addr] = (e, n)
                    # Kirim kunci publik server ke klien
                    server.sendto(f"{public_key[0]},{public_key[1]}".encode(), addr)
                else:
                    if message.decode().startswith("PASSWORD:"):
                        encrypted_pass = message.decode().split(":", 1)[1].strip()
                        entered_pass = decrypt(encrypted_pass, private_key)
                        print(f"entered_pass: {entered_pass}")
                    
                        if (entered_pass == PASSWORD):
                            auth_clients[addr] = True
                            server.sendto("Password benar! Anda berada di obrolan".encode(), addr)
                            #messages.put((f"SIGNUP_TAG:{username_map[addr]}".encode(), addr))
                        else:
                            server.sendto("Password salah! Coba lagi.".encode(), addr)
                    else:
                        server.sendto("Masukkan password dengan format PASSWORD:<password>".encode(), addr)

            else:
                #if addr not in username_map:
                    if message.decode().startswith("CHECK_USERNAME:"):
                        username = message.decode().split(":")[1].strip()
                        if username in usernames:
                            server.sendto("Username unavailable".encode(), addr)
                        else:
                            server.sendto("Username available".encode(), addr)

                    elif message.decode().startswith("SET_USERNAME:"):
                        username = message.decode().split(":")[1].strip()
                        if username in usernames:
                            server.sendto("Username unavailable".encode(), addr)
                        else:
                            usernames.add(username)
                            username_map[addr] = username
                            server.sendto(f"Username {username} berhasil diset!".encode(), addr)
                            messages.put((f"SIGNUP_TAG:{username}".encode(), addr))
                
                    elif message.decode().startswith("SIGNUP_TAG:"):
                        messages.put((message, addr))

                    elif message.decode().startswith("LEAVE_TAG"):
                        username = username_map.get(addr, "Unknown")
                        if addr in clients:
                            clients.remove(addr)
                        if addr in username_map:
                            usernames.rempve(username_map[addr])
                            del username_map[addr]
                        if addr in auth_clients:
                            del auth_clients[addr]
                        broadcast_message = f"{username} keluar dari obrolan."
                        messages.put((broadcast_message.encode(), None))

                    else:
                        encrypted_message = message.decode()
                        decrypted_message = decrypt(encrypted_message, private_key)
                        messages.put((decrypted_message.encode(), addr))    
                
        except:
            pass

def send_message(client, message):
    # batesin ukuran buat dikirim ke klien
    max_size = 1000  # maks ukuran tiap bagian pesan
    for i in range(0, len(message), max_size):
        chunk = message[i:i + max_size]
        # tambahin end buat pesan di akhir
        if i + max_size >= len(message):
            chunk += "END"
        server.sendto(chunk.encode(), client)

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print("Broadcasting message:", message.decode())

            if addr and addr not in clients:
                clients.append(addr)

            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG:"):
                        username = message.decode().split(":")[1].strip()
                        if client != addr:
                            encrypted_message = encrypt(f"{username} memasuki obrolan!", client_public_keys[client])
                            send_message(client, f"ENCRYPTED:{encrypted_message}")
                    else:
                        encrypted_message = encrypt(message.decode(), client_public_keys[client])
                        send_message(client, f"ENCRYPTED:{encrypted_message}")
                except Exception as e:
                    print(f"Error sending message to client {client}: {e}")
                    if client in clients:
                        clients.remove(client)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()