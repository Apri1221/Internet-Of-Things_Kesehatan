# AJT_Kesehatan
Menggunakan library bluepy dan paho mqtt sebagai gateway dan library BLE ESP32 sebagai node sensor
Data dikirimkan menggunakan thingspeak pada alamat : https://thingspeak.com/channels/769763

Tugas ini dikerjakan bersama oleh :
Apriyanto - Fadel - Denny - Muhajir - Mahdiaffan

Dengan arahan bapak Adhitya Bhawiyuga

Semua penjelasan kurang lebih ada di dalam source code

Urutan instruksi untuk menjalankan gateway (Laptop)
 1. install bluepy (untuk python3)
     a. pip bluepy sudo pip3 install bluepy
     b. sudo apt-get install bluez
 2. jalankan aplikasi
     a. sesuaikan mac address pada Peripheral dengan mac esp32 sensor
     b. sesuaikan service uuid dan characteristic uuid
     c. sudo hciconfig hci0 up
     d. sudo python3 [bleGateway.py]
     selesai
