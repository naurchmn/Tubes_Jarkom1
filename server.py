import socket
import threading
import queue


messages = queue.Queue()
clients = []
PASSWORD = "12345"
auth_clients={}

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
                        messages.put((f"SIGNUP_TAG:{addr[0]}".encode(), addr))
                    else:
                        server.sendto("Password salah! Coba lagi.".encode(), addr)
                else:
                    server.sendto("Masukkan password dengan format PASSWORD:<password>".encode(), addr)

            else:
                messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr= messages.get()
            print(message.decode())

            if addr not in clients:
                clients.append(addr)

            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG:"):
                        username = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{username} memasuki obrolan!". encode(), client)
                    elif message.decode().startswith("LEAVE_TAG:"):
                        username = message.decode()[message.decode().index(":")+1:]
                        clients.remove(addr)
                        broadcast_message = f"{username} keluar dari obrolan."
                        for client in clients:
                            server.sendto(broadcast_message.encode(), client)
                    else:
                        print("Pesan dikirim")
                        server.sendto(f"{message.decode()}". encode(), client)
                except:
                    clients.remove(client)
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()