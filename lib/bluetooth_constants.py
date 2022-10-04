#!/usr/bin/python3

ADAPTER_NAME = "hci0"
ADAPTER_HCI1 = "hci1"
ADAPTER_HCI0 = "hci0"
BLUEZ_SERVICE_NAME = "org.bluez"
BLUEZ_NAMESPACE = "/org/bluez/"
DBUS_OM_PROPERTIES="org.freedesktop.DBus.Properties"
DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'

ADAPTER_INTERFACE = BLUEZ_SERVICE_NAME + ".Adapter1"
DEVICE_INTERFACE = BLUEZ_SERVICE_NAME + ".Device1"
GATT_MANAGER_INTERFACE = BLUEZ_SERVICE_NAME + ".GattManager1"
GATT_SERVICE_INTERFACE = BLUEZ_SERVICE_NAME + ".GattService1"
GATT_CHARACTERISTIC_INTERFACE = BLUEZ_SERVICE_NAME + ".GattCharacteristic1"
GATT_DESCRIPTOR_INTERFACE = BLUEZ_SERVICE_NAME + ".GattDescriptor1"
ADVERTISEMENT_INTERFACE = BLUEZ_SERVICE_NAME + ".LEAdvertisement1"
ADVERTISING_MANAGER_INTERFACE = BLUEZ_SERVICE_NAME + ".LEAdvertisingManager1"

RESULT_OK = 0
RESULT_ERR = 1
RESULT_ERR_NOT_CONNECTED = 2
RESULT_ERR_NOT_SUPPORTED = 3
RESULT_ERR_SERVICES_NOT_RESOLVED = 4	
RESULT_ERR_WRONG_STATE = 5
RESULT_ERR_ACCESS_DENIED = 6
RESULT_EXCEPTION = 7
RESULT_ERR_BAD_ARGS = 8
RESULT_ERR_NOT_FOUND = 9

UUID_NAMES = {
    "00001800-0000-1000-8000-00805f9b34fb" : "1800 Generic Access Service",
    "00001801-0000-1000-8000-00805f9b34fb" : "1801 Generic Attribute Service",
    "0000180a-0000-1000-8000-00805f9b34fb" : "180a Device Information Service",
    "0000180f-0000-1000-8000-00805f9b34fb" : "180f Battery Service",
    "0000fe59-0000-1000-8000-00805f9b34fb" : "fe59 Secure DFU Service",
    "e95d93b0-251d-470a-a062-fa1922dfa9a8" : "DFU Control Service",
    "e95d93af-251d-470a-a062-fa1922dfa9a8" : "Event Service",
    "e95d9882-251d-470a-a062-fa1922dfa9a8" : "Button Service",
    "e95d6100-251d-470a-a062-fa1922dfa9a8" : "Temperature Service",
    "e95dd91d-251d-470a-a062-fa1922dfa9a8" : "LED Service",
    "00002a05-0000-1000-8000-00805f9b34fb" : "Service Changed",
    "e95d93b1-251d-470a-a062-fa1922dfa9a8" : "DFU Control",
    "00002a05-0000-1000-8000-00805f9b34fb" : "Service Changed",
    "00002a24-0000-1000-8000-00805f9b34fb" : "Model Number String",
    "00002a25-0000-1000-8000-00805f9b34fb" : "Serial Number String",
    "00002a26-0000-1000-8000-00805f9b34fb" : "Firmware Revision String",
    "e95d9775-251d-470a-a062-fa1922dfa9a8" : "micro:bit Event",
    "e95d5404-251d-470a-a062-fa1922dfa9a8" : "Client Event",
    "e95d23c4-251d-470a-a062-fa1922dfa9a8" : "Client Requirements",
    "e95db84c-251d-470a-a062-fa1922dfa9a8" : "micro:bit Requirements",
    "e95dda90-251d-470a-a062-fa1922dfa9a8" : "Button A State",
    "e95dda91-251d-470a-a062-fa1922dfa9a8" : "Button B State",
    "e95d9250-251d-470a-a062-fa1922dfa9a8" : "Temperature",
    "e95d93ee-251d-470a-a062-fa1922dfa9a8" : "LED Text",
    "00002902-0000-1000-8000-00805f9b34fb" : "Client Characteristic Configuration",
    "6e400001-b5a3-f393-e0a9-e50e24dcca9e" : "Nordic UART Service",
    "98ec1400-00e3-b74f-b2a8-d4e4a0c22036" : "Kosha Device Configuration Service",
    "8ec90003-f315-4f60-9fb8-838830daea50" : "Buttonless DFU without bonds",
    "98ec1407-00e3-b74f-b2a8-d4e4a0c22036" : "Sampling?",
    "98ec1409-00e3-b74f-b2a8-d4e4a0c22036" : "1409 ",
    "98ec1404-00e3-b74f-b2a8-d4e4a0c22036" : "1404 ",
    "98ec1403-00e3-b74f-b2a8-d4e4a0c22036" : "1403 ",
    "98ec1402-00e3-b74f-b2a8-d4e4a0c22036" : "1402 Sampling time secs",
    "98ec1401-00e3-b74f-b2a8-d4e4a0c22036" : "1401 ODR ",
    "6e400003-b5a3-f393-e0a9-e50e24dcca9e" : "UART Tx",
    "6e400002-b5a3-f393-e0a9-e50e24dcca9e" : "UART Rx",

}    


UART_SERVICE = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHRC = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UART_TX_CHRC = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

CONFIG_SERVICE = "98ec1400-00e3-b74f-b2a8-d4e4a0c22036"
CONF_1401 = "98ec1401-00e3-b74f-b2a8-d4e4a0c22036"
CONF_1402 = "98ec1402-00e3-b74f-b2a8-d4e4a0c22036"
CONF_1403 = "98ec1403-00e3-b74f-b2a8-d4e4a0c22036"
CONF_1405 = "98ec1405-00e3-b74f-b2a8-d4e4a0c22036"
CONF_1407 = "98ec1407-00e3-b74f-b2a8-d4e4a0c22036"
CONF_1409 = "98ec1409-00e3-b74f-b2a8-d4e4a0c22036"

CHRC_CONFIG = [
    "98ec1407-00e3-b74f-b2a8-d4e4a0c22036",
    "98ec1409-00e3-b74f-b2a8-d4e4a0c22036",
    "98ec1404-00e3-b74f-b2a8-d4e4a0c22036",
    "98ec1403-00e3-b74f-b2a8-d4e4a0c22036",
    "98ec1402-00e3-b74f-b2a8-d4e4a0c22036",
    "98ec1401-00e3-b74f-b2a8-d4e4a0c22036",
    ]

DEVICE_INF_SVC_UUID = "0000180a-0000-1000-8000-00805f9b34fb"
MODEL_NUMBER_UUID    = "00002a24-0000-1000-8000-00805f9b34fb"

TEMPERATURE_SVC_UUID = "e95d6100-251d-470a-a062-fa1922dfa9a8"
TEMPERATURE_CHR_UUID = "e95d9250-251d-470a-a062-fa1922dfa9a8"

LED_SVC_UUID = "e95dd91d-251d-470a-a062-fa1922dfa9a8"
LED_TEXT_CHR_UUID = "e95d93ee-251d-470a-a062-fa1922dfa9a8"

MANUFACTURER_NAMES = {
    '87': 'Garmin International Inc',
    '4C' : 'Apple Inc'
}