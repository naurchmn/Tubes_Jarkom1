import socket
import threading
import random
from rsa_module import generate_keys, encrypt, decrypt

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("0.0.0.0", random.randint(8000, 9000)))

# get hostname sama ip
hostname= socket.gethostname()
IP = socket.gethostbyname(hostname)
# generate public key and private key klien
public_key, private_key = generate_keys()


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

client.sendto(f"{public_key[0]},{public_key[1]}".encode(), server_address)
# Terima kunci publik server
message, _ = client.recvfrom(1024)
e, n = map(int, message.decode().split(","))
server_public_key = (e, n)

def receive_full_message():
    message_parts = []
    while True:
        try:
            packet, _ = client.recvfrom(1024)
            if b"END" in packet:
                message_parts.append(packet.replace(b"END", b""))
                break
            else:
                message_parts.append(packet)
        except Exception as e:
            print(f"Error saat menerima paket: {e}")
            break
    full_message = b"".join(message_parts)
    return full_message.decode()



def receive():
    while True:
        try:
            full_message = receive_full_message()
            if full_message.startswith("ENCRYPTED:"):
                encrypted_message_hex = full_message.replace("ENCRYPTED:", "").strip()
                decrypted_message = decrypt(encrypted_message_hex, private_key)
                print(decrypted_message)
            else:
                print(f"Server message: {full_message}")
        except Exception as e:
            print(f"Error saat menerima atau mendekripsi pesan: {e}")

print(f"Your IP: {IP}")

while True:
    password = input("Password: ")
    try:
        encrypted_password = encrypt(password, server_public_key)
        client.sendto(f"PASSWORD:{encrypted_password}".encode(), server_address)
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
            break
        else:
            print("Password salah, coba lagi.")
        
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
        encrypted_message = encrypt(f"{username}: {message}", server_public_key)
        client.sendto(str(encrypted_message).encode(), server_address)