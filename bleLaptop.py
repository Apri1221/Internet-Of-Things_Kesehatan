# Source code ini untuk ujicoba BLE pada Laptop (Linux)


# ----------------------- 1. Untuk mendapatkan data dari ESP32 ---------------------------
# https://github.com/orientlu/bluepy/blob/master/test.py

# import binascii
# import struct
# import time
# from bluepy.btle import UUID, Peripheral

# temp_uuid = UUID(0x2221)

# p = Peripheral("24:0A:C4:AE:85:A2", "random")

# try:
#     ch = p.getCharacteristics(uuid=temp_uuid)[0]
#     if (ch.supportsRead()):
#         while 1:
#             val = binascii.b2a_hex(ch.read())
#             val = binascii.unhexlify(val)
#             val = struct.unpack('f', val)[0]
#             print(str(val) + " deg C")
#             time.sleep(1)

# finally:
#     p.disconnect()






# ------------------------- 2. Ini untuk scan device yang ada ----------------------------
# memberikan informasi : Device 24:0a:c4:ae:85:a2(public), RSSI=-54 dB
# dengan bagian pertama adalah alamat device, (type address), RSSI
# type addres ada public (static atau private), dan random
# selengkapnya ada di https://github.com/rlangoy/bluepy_examples_nRF51822_mbed/blob/master/BLE40_bluepy_slides.pdf

# from bluepy.btle import Scanner

# scanner = Scanner()
# devices = scanner.scan(10)

# for dev in devices:
#     print ("Device %s(%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
#     for (adtype, desc, value) in dev.getScanData():
#         print(" %s = %s" % (desc,value))






# ------------------------- 3. ini mencoba untuk melihat characteristic (fungsi yang ada pada BLE) -------------------
# akan print semua UUID yang ada di dalam BLE Device tersebut
# saat melakukan get characteristic, serial monitor BLE berfungsi (terlihat dia print humidity)
# namun setelah selesai dapatin semua characteristic, serial monitor berhenti looping dan ada bacaan start advertising
# setiap kali dilakukan get characteristic di bluepy, BLE ESP32 looping dht11
# jika UUID nya berupa aneh, maka itu tidak terdefenisi pada bluetooth.org

# from bluepy.btle import UUID, Peripheral

# # p = Peripheral(sys.argv[1],"random")
# p = Peripheral("24:0A:C4:AE:85:A2","public")

# services=p.getServices()

# #displays all services
# for service in services:
#    print(service)


# root@apriaja:/media/apri/New Volume/Semester 6/AJT/tugas akhir# sudo python3 bleLaptop.py
# Service <uuid=Generic Attribute handleStart=1 handleEnd=5>
# Service <uuid=Generic Access handleStart=20 handleEnd=28>
# Service <uuid=6e400001-b5a3-f393-e0a9-e50e24dcca9e handleStart=40 handleEnd=65535>






# ------------------- 4. Untuk mendapatkan descriptor service yang ada pada device lain (ESP32) ----------------------
# from bluepy.btle import UUID, Peripheral

# # p = Peripheral(sys.argv[1],"random")
# p = Peripheral("24:0A:C4:AE:85:A2","public")

# descriptors=p.getDescriptors(1,0x00F) #Bug if no limt is specified the function wil hang
# 				      # (go in a endless loop and not return anything)
# print("UUID                                  Handle UUID by name")
# for descriptor in descriptors:
#    print ( " "+ str(descriptor.uuid) + "  0x" + format(descriptor.handle,"02X") +"   "+ str(descriptor) )

# root@apriaja:/media/apri/New Volume/Semester 6/AJT/tugas akhir# sudo python3 bleLaptop.py
# UUID                                  Handle  UUID by name
#  00002800-0000-1000-8000-00805f9b34fb  0x01   Descriptor <Primary Service Declaration>
#  00002803-0000-1000-8000-00805f9b34fb  0x02   Descriptor <Characteristic Declaration>
#  00002a05-0000-1000-8000-00805f9b34fb  0x03   Descriptor <Service Changed>
#  00002902-0000-1000-8000-00805f9b34fb  0x04   Descriptor <Client Characteristic Configuration>






# ---------------------- 5. Source code untuk melihat kemampuan service yang ada pada BLE lain ---------------------
# from bluepy.btle import UUID, Peripheral

# # p = Peripheral(sys.argv[1],"random")
# p = Peripheral("24:0A:C4:AE:85:A2","public")

# chList = p.getCharacteristics()
# print ("Handle   UUID                                Properties")
# print ("-------------------------------------------------------")
# for ch in chList:
#    print ("  0x"+ format(ch.getHandle(),'02X')  +"   "+str(ch.uuid) +" " + ch.propertiesToString())

# pengembaliannya akan berupa :
# Handle   UUID                                Properties
# -------------------------------------------------------
#   0x03   00002a05-0000-1000-8000-00805f9b34fb INDICATE
#   0x16   00002a00-0000-1000-8000-00805f9b34fb READ
#   0x18   00002a01-0000-1000-8000-00805f9b34fb READ
#   0x1A   00002aa6-0000-1000-8000-00805f9b34fb READ
#   0x2A   ff84a84e-857b-4827-8ef1-35cd19b41669 READ NOTIFY
#   0x2D   82934e82-e8e3-4c55-b3f4-55ace378812f WRITE

# selanjutnya perhatikan UUID
# Service <uuid=6e400001-b5a3-f393-e0a9-e50e24dcca9e handleStart=40 handleEnd=65535>
# dev_name_uuid = UUID(6e400001-b5a3-f393-e0a9-e50e24dcca9e)

# dan characteristicnya -> ff84a84e-857b-4827-8ef1-35cd19b41669 / 82934e82-e8e3-4c55-b3f4-55ace378812f
# dev_char_uuid = UUID(ff84a84e-857b-4827-8ef1-35cd19b41669)






# ---------------------- 6. berhasil connect dan menampilkan data (namun hanya 1 device) ---------------------------

# import binascii
# import struct
# import time
# from bluepy.btle import UUID, Peripheral

# button_service_uuid = UUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b")
# button_char_uuid    = UUID("beb5483e-36e1-4688-b7f5-ea07361b26a8")

# # p = Peripheral(sys.argv[1],"random")
# p = Peripheral("24:0A:C4:AE:85:A2","public")

# ButtonService=p.getServiceByUUID(button_service_uuid)

# try:
#     ch = ButtonService.getCharacteristics(button_char_uuid)[0]
#     if (ch.supportsRead()):
#         while 1:
#             val = binascii.b2a_hex(ch.read())
#             val = binascii.unhexlify(val)
#             print ("Data : " + str(val))
#             # keluarannya -> b'-14, 166'
#             # b ini menunjukkan datanya adalah bytes yg diconvert ke string
#             # you need to decode the bytes of you want a string:
#             # b = b'1234'
#             # print(b.decode('utf-8'))  # '1234'

# finally:
#     p.disconnect()




# ---------------------------  7. Berhasil untuk mendapatkan data secara multikoneksi --------------------------
from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import threading
import binascii
import time

# dht, jantung/pulse, pir
bt_addrs = ['24:0a:c4:ae:85:a2', '3c:71:bf:4c:a8:7e', '30:ae:a4:26:8d:96']
UUID_service = ["4fafc201-1fb5-459e-8fcc-c5c9c331914b"]
UUID_ch = ["beb5483e-36e1-4688-b7f5-ea07361b26a8"]
scanner = Scanner(0)

# buat variabel global
field = {}
field[0] = ''
field[1] = ''
field[2] = ''
field[3] = ''


def aturfield(mac_addr, val):
    tuples = val.split(',')
    if mac_addr == "24:0a:c4:ae:85:a2":
        i = 0
        # i = 0 adalah suhu
        # i = 1 adalah kelembaban
        for tuple in tuples:
            field[i] = tuple
            i += 1
    elif mac_addr == "3c:71:bf:4c:a8:7e":
        i = 2
        # i = 2 adalah denyut jantung
        for tuple in tuples:
            field[i] = tuple
            i += 1
    elif mac_addr == "30:ae:a4:26:8d:96":
        i = 3
        # i = 3 adalah nilai gerak
        for tuple in tuples:
            field[i] = tuple
            i += 1



def handle_notifikasi(mac_addr, ch):
    while True:  # <-- maintain terus koneksinya
        try:
            # cek mac_addr yg dikirim apa
            # untuk mac_addr tertentu maka field nya disesuaikan jumlah nya
            if (ch.supportsRead()):
                while 1:
                    val = binascii.b2a_hex(ch.read())
                    val = binascii.unhexlify(val)
                    val = val.decode('utf-8')
                    # keluarannya -> b'-14, 166'
                    # b ini menunjukkan datanya adalah bytes yg diconvert ke string
                    # b = b'1234'
                    # print(b.decode('utf-8'))  # '1234'

                    # pisah menjadi beberapa tupple berdasarkan devicenya
                    # tuples = val.split(',')
                    # i = 0
                    aturfield(mac_addr, val)

                    # dht
                    print("Data dari device " + str(mac_addr) + " : " + field[0] + ', ' + field[1] + ', ' + field[2] + ', ' + field[3])
                    

        except:
            print("Data error, kemungkinan data tidak terbaca")
        
        # harus di disconnect dulu bluetoothnya karena client tidak bisa me-mantain banyak koneksi
        finally:
            p.disconnect()
            # stop masuk ke looping lagi dengan break looping
            break


while True:
    print('Scanning...')
    # lakukan Scann
    devices = scanner.scan()

    # lakukan looping, masukkan tiap device yang ada dari scan
    for d in devices:
        print(d.addr)
        # jika alamat yg di scan ada di alamat yg terdaftar
        # lakukan sesuatu
        if d.addr in bt_addrs:
            # a = bt_addrs.index(d.addr)
            # print(a)
            service = UUID_service[0]
            char = UUID_ch[0]

            try:
                # lakukan koneksi ke MAC device
                p = Peripheral(d, "public")

                # pair ke service dan characteristic device
                Service = p.getServiceByUUID(service)
                ch = Service.getCharacteristics(char)[0]

                # kirimkan ch (finalnya pairing bluetooth) ke parameter fungsi thread
                # looping di thread untuk menerima notifikasi
                t = threading.Thread(target=handle_notifikasi, args=(d.addr, ch,))
                t.start()
                # dapatin data dulu selama 2 detik sebelum masuk ke mac_addr device berikutnya
                time.sleep(10)
                # setelah selesai, akan memanggil finally pada fungsi thread, lalu masuk ke device berikutnya dari hasil scan
            except:
                p.disconnect()