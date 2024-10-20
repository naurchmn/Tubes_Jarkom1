import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("0.0.0.0", random.randint(8000, 9000)))

username= input("Username:")
hostname= socket.gethostname()
IP = socket.gethostbyname(hostname)
print(f"Your IP: {IP}")

def get_valid_port():
    while True:
        try:
            sendPORT= int(input("Port: "))
            if 0<= sendPORT<=65535:
                if sendPORT !=9999:
                    while True:
                        pilih = input(f"Port yang anda masukkan bukan port server kami (9999)."
                                      f"Anda ingin melanjutkan dengan port {sendPORT}? (y/n):").lower()
                        if pilih == 'n':
                            return 9999
                        elif pilih =='y':
                            return sendPORT
                        else:
                            print ("pilihan tidak valid, coba lagi.")
                else:
                    return sendPORT
            else:
                print("Port harus dalam rentang 0-65535, coba lagi.")
        except ValueError:
            print("Port yang dimasukkan tidak valid. Harus berupa angka, coba kembali")
def get_valid_IP():
    while True:
        sendIP=input("IP: ")
        try:
            socket.inet_aton(sendIP)
            return sendIP
        except socket.error:
            print("IP Address tidak valid, coba lagi")
sendPORT = get_valid_port()
sendIP = get_valid_IP()
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