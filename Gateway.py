# sudah menggabungkan BLE dengan MQTT [Gateway]

from __future__ import print_function
import paho.mqtt.publish as publish
import string
import random

from bluepy.btle import Scanner, Peripheral
import threading
import binascii
import time


# --------------- settingan bluetooth ------------------
# dht, jantung/pulse, pir
bt_addrs = ['24:0a:c4:ae:85:a2', '3c:71:bf:4c:a8:7e', '30:ae:a4:26:8d:96']
# buat semua device memiliki service dan characteristic yang sama dengan ini
UUID_service = ["4fafc201-1fb5-459e-8fcc-c5c9c331914b"]
UUID_ch = ["beb5483e-36e1-4688-b7f5-ea07361b26a8"]
scanner = Scanner(0)

# buat variabel global
# field[0] = suhu, field[1] = kelembaban dan seterusnya
# buat variabel global
field = {}
field[0] = ''
field[1] = ''
field[2] = ''
field[3] = ''


# --------------- Untuk komunikasi ke Thingspeak -----------------------
string.alphanum = '1234567890abcdefghijklmnopqrstuvwxyzxABCDEFGHIJKLMNOPQRSTUVWXYZ'

# The ThingSpeak Channel ID.
# Replace <YOUR-CHANNEL-ID> with your channel ID.
channelID = "769763"

# The Write API Key for the channel.
# Replace <YOUR-CHANNEL-WRITEAPIKEY> with your write API key.
writeAPIKey = "T14MNQO3Y586EKYH"

# The Hostname of the ThingSpeak MQTT broker.
mqttHost = "mqtt.thingspeak.com"

# You can use any Username.
mqttUsername = "ESP32MQTTDemo2"

# Your MQTT API Key from Account > My Profile.
mqttAPIKey = "WG8RJSDLILMJ4ICQ"

# --------------- Akhir dari set komunikasi ke Thingspeak -------------------


# ----------------- Model Komunikasi dengan websocket/TCP/MQTT -------------------

# pada thread ini : https://community.thingspeak.com/tutorials/update-a-thingspeak-channel-using-mqtt-on-a-raspberry-pi/

# NOTE kita harus milih salah satu yang True

# Set useUnsecuredTCP to True to use the default MQTT port of 1883
# This type of unsecured MQTT connection uses the least amount of system resources.
useUnsecuredTCP = True

# Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.
# Try this if port 1883 is blocked on your network.
useUnsecuredWebsockets = False

# Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
# This type of connection will use slightly more system resources, but the connection
# will be secured by SSL.
useSSLWebsockets = False

# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None

if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs': "/etc/ssl/certs/ca-certificates.crt",'tls_version': ssl.PROTOCOL_TLSv1}
    tPort = 443

# --------------- Akhir dari set komunikasi ---------------------


# Create the topic string.
topic = "channels/" + channelID + "/publish/" + writeAPIKey


# ---------------- Generate client ID sekali secara random ----------------
clientID = ''
# Create a random clientID.
# NOTE ini di random dari isi alphanum dengan fungsi random
for x in range(1, 16):
    clientID += random.choice(string.alphanum)



def aturfield(mac_addr, val):
    tuples = val.split(',')
    if mac_addr == "24:0a:c4:ae:85:a2":
        i = 0
        # i = 0 adalah suhu
        # i = 1 adalah kelembaban
        field[2] = ''
        field[3] = ''
        for tuple in tuples:
            field[i] = tuple
            i += 1
    elif mac_addr == "3c:71:bf:4c:a8:7e":
        i = 2
        # i = 2 adalah denyut jantung
        field[0] = ''
        field[1] = ''
        field[3] = ''
        for tuple in tuples:
            field[i] = tuple
            i += 1
    elif mac_addr == "30:ae:a4:26:8d:96":
        i = 3
        # i = 3 adalah nilai gerak
        field[0] = ''
        field[1] = ''
        field[2] = ''
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
                    # if mac_addr = sesuatu, mulai i dari berapa gitu
                    aturfield(mac_addr, val)

                    # print("Data dari device " + str(mac_addr) + " : " + field[0] + ',' + field[1])

                    # mulai kirimkan data ke mqtt
                    # silahkan sediakan dan labelkan di Thingspeak pada n field
                    payload = "field1=" + str(field[0]) + "&field2=" + str(field[1]) + "&field3=" + str(field[2]) + "&field4=" + str(field[3])

                    # attempt to publish this data to the topic.
                    publish.single(topic, payload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport, auth={'username': mqttUsername, 'password': mqttAPIKey})
                    print("Published Suhu =", field[0], " Kelembaban =", field[1], " Jantung =", field[2]," Gerak =", field[3]," to host: ", mqttHost, " clientID= ", clientID)
        
        except:
            print("Data error, kemungkinan data tidak terbaca")
        
        # harus di disconnect dulu bluetoothnya karena client tidak bisa me-mantain banyak koneksi
        finally:
            p.disconnect()
            # stop masuk ke looping lagi dengan break looping
            break


while True:
    print('\nScanning...')
    # lakukan scan, sebenarnya tanpa parameter karena kita hanya scan kembali ketika telah selesai looping for
    # tapi tidak tahu kenapa, ketika data dari esp32 tidak terbaca, bluetooth langsung dimatikan dan tidak akan pernah selamanya menerima data
    # namun jika diberi 10 detik jeda untuk scan, kita masih punya kemungkinan mendapat data dari esp32, kenapa ya?
    devices = scanner.scan()

    # lakukan looping for, masukkan tiap device yang ada dari scan
    for d in devices:
        print(d.addr)
        # jika alamat yg di scan ada di alamat yg terdaftar
        # lakukan sesuatu
        if d.addr in bt_addrs:
            # a = bt_addrs.index(d.addr)
            # print(a)
            service = UUID_service[0]
            char = UUID_ch[0]
            
            # lakukan koneksi ke MAC device
            p = Peripheral(d)

            try:
                # pair ke service dan characteristic device
                Service = p.getServiceByUUID(service)
                ch = Service.getCharacteristics(char)[0]

                # kirimkan ch (finalnya pairing bluetooth) ke parameter fungsi thread
                # looping di thread untuk menerima notifikasi
                t = threading.Thread(target=handle_notifikasi, args=(d.addr, ch,))
                t.start()

                # dapatin data dulu selama 10 detik sebelum masuk ke mac_addr device berikutnya
                time.sleep(10)
                # setelah selesai, akan memanggil finally pada fungsi thread, lalu masuk ke device berikutnya dari hasil scan
            except:
                # jika terjadi error, putuskan langsung
                p.disconnect()