import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("0.0.0.0", random.randint(8000, 9000)))


hostname= socket.gethostname()
IP = socket.gethostbyname(hostname)
def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass
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
            if sendIP.count('.')==3:
                return sendIP
            else:
                print("Format IP address tidak valid, coba lagi")
        except socket.error:
            print("IP Address tidak valid, coba lagi")

sendPORT = get_valid_port()
sendIP = get_valid_IP()
server_address = (sendIP, sendPORT)

print(f"Your IP: {IP}")

password = input("Password: ")
try:
    client.sendto(f"PASSWORD:{password}".encode(), server_address)
    message, _ = client.recvfrom(1024)
    response = message.decode()
    print(f"Server response: {response}")
    if response == "Password benar! Anda berada di obrolan":
        while True:
            username = input("Username: ")
            client.sendto(f"CHECK_USERNAME:{username}".encode(), server_address)
            
            print("Checking username availability...")
            
            message, _ = client.recvfrom(1024)
            response = message.decode()

            print(f"Server response: {response}")
            
            if response == "Username available":
                client.sendto(f"SET_USERNAME:{username}".encode(), server_address)
                confirmation, _ = client.recvfrom(1024)
                print(confirmation.decode())
                break
            
            elif response == "Username unavailable":
                print("Username sudah terdaftar, silakan masukkan username yang lain.")
            else:
                print("Unexpected response from server.")
        print(f"Selected username: {username}")
        
        t = threading.Thread(target=receive)
        t.start()

        client.sendto(f"SIGNUP_TAG:{username}".encode(), server_address)
    else:
        print("Password salah, coba lagi.")
        exit()
    
except Exception as e:
     print(f"Error saat mengirim password: {e}")
     exit()

client.sendto(f"SIGNUP_TAG:{username}".encode(), server_address)

while True:
    message = input("")
    if message == "!q":
        client.sendto(f"LEAVE_TAG:{username}".encode(), server_address)
        exit()
    else:
        client.sendto(f"{username}: {message}".encode(), server_address)