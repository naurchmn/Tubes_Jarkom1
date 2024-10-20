import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("0.0.0.0", random.randint(8000, 9000)))

username= input("Username:")
hostname= socket.gethostname()
IP = socket.gethostbyname(hostname)
print(IP)

sendPORT= int(input("Port: "))
sendIP=input("IP: ")
server_address = (sendIP, sendPORT)

password = input("Password: ")
client.sendto(f"PASSWORD:{password}". encode(), server_address)

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{username}".encode(), server_address)

while True:
    message = input("")
    if message == "!q":
        client.sendto(f"LEAVE_TAG:{username}".encode(), server_address)
        exit()
    else:
        client.sendto(f"{username}: {message}".encode(), server_address)