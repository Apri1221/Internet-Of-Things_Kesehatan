// source code untuk dhtSensor dengan sudah diimplementasikan pada bleNotify

#include <DHT.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

BLEServer *pServer = NULL;
BLECharacteristic *pCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;
uint32_t value = 0;

/*
    Definition of DHT11
*/

#define DHTTYPE DHT11 // sets sensor type, in case DHT11
#define DHTPIN 4      // DHT11 data pin

DHT dht(DHTPIN, DHTTYPE);

int humidity;
int temperature;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

class MyServerCallbacks : public BLEServerCallbacks
{
    void onConnect(BLEServer *pServer)
    {
        deviceConnected = true;
    };

    void onDisconnect(BLEServer *pServer)
    {
        deviceConnected = false;
    }
};

void setup()
{
    Serial.begin(115200);

    // Create the BLE Device
    BLEDevice::init("ESP32 Apri");

    // Create the BLE Server
    pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());

    // Create the BLE Service
    BLEService *pService = pServer->createService(SERVICE_UUID);

    // Create a BLE Characteristic
    pCharacteristic = pService->createCharacteristic(
        CHARACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_READ |
            BLECharacteristic::PROPERTY_WRITE |
            BLECharacteristic::PROPERTY_NOTIFY |
            BLECharacteristic::PROPERTY_INDICATE);

    // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
    // Create a BLE Descriptor
    pCharacteristic->addDescriptor(new BLE2902());

    // Start the service
    pService->start();

    // Start advertising
    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->setScanResponse(false);
    pAdvertising->setMinPreferred(0x0); // set value to 0x00 to not advertise this parameter
    BLEDevice::startAdvertising();
    Serial.println("Waiting a client connection to notify...");
}

void loop()
{
    // notify changed value
    if (deviceConnected)
    {
        // tentang suhu
        humidity = dht.readHumidity();
        temperature = dht.readTemperature();
        // testa se retorno é valido, caso contrário algo está errado.
        if (isnan(temperature) || isnan(humidity))
        {
            Serial.println("Failed to read from DHT");
        }
        else
        {
            Serial.print("Humidity: ");
            Serial.print(humidity);
            Serial.print(" %\t");
            Serial.print("Temperature: ");
            Serial.print(temperature);
            Serial.println(" *C");
        }

        char humidityString[2];
        char temperatureString[2];
        dtostrf(humidity, 1, 2, humidityString);
        dtostrf(temperature, 1, 2, temperatureString);

        char dhtDataString[16];
        sprintf(dhtDataString, "%d,%d", temperature, humidity);

        //    pTxCharacteristic->setValue(&txValue, 1);
        pCharacteristic->setValue(dhtDataString);
        pCharacteristic->notify();

        Serial.print("*** Sent Data: ");
        Serial.print(dhtDataString);
        Serial.println("***");
        delay(500); // bluetooth stack will go into congestion, if too many packets are sent, in 6 hours test i was able to go as low as 3ms
    }
    // disconnecting
    if (!deviceConnected && oldDeviceConnected)
    {
        delay(500);                  // give the bluetooth stack the chance to get things ready
        pServer->startAdvertising(); // restart advertising
        Serial.println("start advertising");
        oldDeviceConnected = deviceConnected;
    }
    // connecting
    if (deviceConnected && !oldDeviceConnected)
    {
        // do stuff here on connecting
        oldDeviceConnected = deviceConnected;
    }
}