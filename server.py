import socket
import threading
import queue


messages = queue.Queue()
clients = []
PASSWORD = "12345"
auth_clients={}
usernames = set()
username_map = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 9999))


def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)

            if addr not in auth_clients:
                if message.decode().startswith("PASSWORD:"):
                    entered_pass = message.decode().split(":")[1].strip()
                    if entered_pass == PASSWORD:
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
                        messages.put((message, addr))
                
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr= messages.get()
            print(message.decode())

            if addr and addr not in clients:
                clients.append(addr)

            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG:"):
                        username = message.decode()[message.decode().index(":")+1:]
                        if client != addr:  # Don't send to the user who just joined
                            server.sendto(f"{username} memasuki obrolan!".encode(), client)
                       
                    else:
                        print("Pesan dikirim")
                        server.sendto(message, client)

                    '''else:
                        print("Pesan dikirim")
                        server.sendto(f"{message.decode()}".encode(), client)'''
                except:
                    if client in clients:
                        clients.remove(client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()