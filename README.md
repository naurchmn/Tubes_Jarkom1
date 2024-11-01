# UDP SOCKET PROGRAMMING

## Deskripsi Program

Program ini adalah aplikasi chat sederhana berbasis **client-server** yang menggunakan protokol **UDP** dan enkripsi **RSA** untuk komunikasi yang aman. Program ini terdiri dari dua file utama: `server.py` dan `client.py`, yang memungkinkan beberapa client untuk berkomunikasi melalui server dengan enkripsi end-to-end.

## Persiapan Program

1. Pastikan bahwa file `server.py` dan `client.py` berada di dalam folder atau direktori yang sama.
2. Pastikan Anda telah menginstal **Python 3.x** di sistem Anda.

---

## Menjalankan Program Server

1. Buka terminal atau command prompt.
2. Navigasikan ke folder tempat file `server.py` berada.
3. Jalankan server dengan perintah berikut:
   ```bash
   python server.py
4. Server akan berjalan pada port 9999 dan akan menunggu koneksi dari client.
5. Saat ada request dari client, server akan meminta password. Default password pada server adalah 12345.
## Menjalankan Server di Laptop Sendiri

Jika Anda ingin menjalankan server di laptop Anda sendiri dan mengizinkan client lain untuk terhubung, Anda perlu mengetahui **IP Address** dari perangkat Anda. Untuk melihat IP Address di Windows, ikuti langkah-langkah berikut:

1. Buka **Command Prompt** (CMD) dengan cara mengetik `cmd` di kolom pencarian Windows dan tekan **Enter**.
2. Di jendela Command Prompt, ketik perintah berikut dan tekan **Enter**:
   ```bash
   ipconfig
3. Temukan bagian **IPv4 Address** di bawah koneksi yang aktif (misalnya, Wi-Fi atau Ethernet). Alamat ini adalah **IP tujuan** yang perlu digunakan oleh client untuk terhubung ke server Anda.

## Menjalankan Program Client

1. Buka terminal atau command prompt.
2. Navigasikan ke folder yang sama di mana file `client.py` berada.
3. Jalankan client dengan perintah berikut:
   ```bash
   python client.py
4. Program client akan meminta input berikut:
   - **Port**: Client dapat memasukkan port yang diinginkan. Jika port yang dimasukkan bukan `9999`, program akan menanyakan apakah ingin tetap melanjutkan dengan port tersebut.
   - **Username**: Pilih username unik yang akan digunakan di obrolan.
   - **Password**: Masukkan password yang sesuai dengan yang diset pada server (`12345` secara default).
5. Jika password benar, client akan berhasil terhubung dengan server dan dapat mulai berkomunikasi dengan client lain.

## Tentang Penulis

Naura Ayurachmani (18223061)  
Noeriza Aqila Wibawa  (18223095)

