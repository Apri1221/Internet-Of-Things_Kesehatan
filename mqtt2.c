// Readme, untuk penjelasan lebih, highlight kata yang bertuliskan NOTE
// source code murni dapat dilihat pada tutorial ini https://www.mathworks.com/help/thingspeak/use-arduino-client-to-publish-to-a-channel.html


#include <SPI.h>
#include "DHT.h"
#include <PubSubClient.h>
#include <WiFi.h>

#define WIFI_AP "RedmiNote7"
#define WIFI_PASSWORD "habispaket"

#define DHTPIN 4      // DHT Sensor connected to digital pin 2.
#define DHTTYPE DHT11 // Type of DHT sensor.

DHT dht(DHTPIN, DHTTYPE); // Initialize DHT sensor.

// berkaitan dengan thingspeak
const char *server = "mqtt.thingspeak.com";

char mqttUserName[] = "ESP32MQTTDemo";   // Can be any name.
char mqttPass[] = "WG8RJSDLILMJ4ICQ";      // Change this your MQTT API Key from Account > MyProfile.
char writeAPIKey[] = "T14MNQO3Y586EKYH"; // Change to your channel Write API Key.
// long channelID = NNNNNN; NOTE ganti dengan channel ID
long channelID = 769763;

static const char alphanum[] = "0123456789"
                               "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                               "abcdefghijklmnopqrstuvwxyz"; // For random generation of client ID.

WiFiClient client;               // Initialize the Wifi client library.
PubSubClient mqttClient(client); // Initialize the PuBSubClient library.

unsigned long lastConnectionTime = 0;
const unsigned long postingInterval = 5L * 1000L; // Post data every 5 seconds.

// setup
void setup()
{
    Serial.begin(115200);
    dht.begin();
    delay(10);
    // koneksi ke wifi
    InitWiFi();
    mqttClient.setServer(server, 1883); // Set the MQTT broker details.
}

// looping
void loop()
{
    // Reconnect if MQTT client is not connected.
    if (!mqttClient.connected())
    {
        reconnect();
    }

    mqttClient.loop(); // Call the loop continuously to establish connection to the server.

    // If interval time has passed since the last connection, Publish data to ThingSpeak
    if (millis() - lastConnectionTime > postingInterval)
    {
        mqttpublish();
    }
}


void InitWiFi()
{
    Serial.println("Connecting to AP ...");
    // attempt to connect to WiFi network

    WiFi.begin(WIFI_AP, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected to AP");
}


// NOTE method reconnect ini bukan untuk koneksi wifi, tp ke channel
void reconnect()
{
    char clientID[9];

    // Loop until we're reconnected
    while (!mqttClient.connected())
    {
        Serial.print("Attempting MQTT connection...");
        // Generate ClientID
        for (int i = 0; i < 8; i++)
        {
            clientID[i] = alphanum[random(51)];
        }
        clientID[8] = '\0';

        // NOTE Connect to the MQTT broker dengan ID dan pass
        if (mqttClient.connect(clientID, mqttUserName, mqttPass))
        {
            Serial.println("connected");
        }
        else
        {
            Serial.print("failed, rc=");
            // Print to know why the connection failed.
            // See https://pubsubclient.knolleary.net/api.html#state for the failure code explanation.
            Serial.print(mqttClient.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

// NOTE method mqtt dipanggil secara periodik di method loop
void mqttpublish()
{
    float t = dht.readTemperature(true);   // Read temperature from DHT sensor.
    float h = dht.readHumidity();          // Read humidity from DHT sensor.
    // int lightLevel = analogRead(LIGHTPIN); // Read from light sensor


    // NOTE penulisan data ke thingspeak punya aturan! yaitu : field1 = nilai1 & field2 = nilai2 & fieldN = nilaiN ...
    // https://www.mathworks.com/help/thingspeak/publishtoachannelfeed.html
    // banyaknya field harus disesuaikan pada thingspeak, jika field yang bakal dikirimkan ke thinsgpeak berjumlah 2 maka pada saat pembuatan channel, jumlah fieldnya harus 2 juga
    // pada thingspeak, field dapat diberi label, misalnya field1 adalah temperatur dan field2 adalah kelembaban

    String data = String("field1=" + String(t, DEC) + "&field2=" + String(h, DEC));
    int length = data.length();
    char msgBuffer[length];
    data.toCharArray(msgBuffer, length + 1);
    Serial.println(msgBuffer);


    // NOTE komposisi untuk menulis di channel adalah channels/ <channelID> /publish/ <apikey>
    // https://www.mathworks.com/help/thingspeak/publishtoachannelfeed.html

    // Create a topic string and publish data to ThingSpeak channel feed.
    String topicString = "channels/" + String(channelID) + "/publish/" + String(writeAPIKey);
    length = topicString.length();
    char topicBuffer[length];
    topicString.toCharArray(topicBuffer, length + 1);

    mqttClient.publish(topicBuffer, msgBuffer);

    lastConnectionTime = millis();
}

// Use this function instead to publish to a single field directly.  Don't forget to comment out the above version.
/*
void mqttpublish() {
  
  float t = dht.readTemperature(true); // Read temperature from DHT sensor.

  String data = String(t, DEC);
  int length = data.length();
  char msgBuffer[length];
  data.toCharArray(msgBuffer,length+1);
  Serial.println(msgBuffer);
  
  // Create a topic string and publish data to ThingSpeak channel feed. 
  String topicString ="channels/" + String( channelID ) + "/publish/"+String(writeAPIKey);
  length=topicString.length();
  char topicBuffer[length];
  topicString.toCharArray(topicBuffer,length+1);
 
  mqttClient.publish( topicBuffer, msgBuffer );

  lastConnectionTime = millis();
}
*/