# Originally Written by @sean-morris (https://github.com/sean-morris), modified by @Nikpol11

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
import io
import time

button_map = {
    ButtonPacket.BUTTON_1: "1", #b'!B11:'
    ButtonPacket.BUTTON_2: "2", #b'!B219'
    ButtonPacket.BUTTON_3: "3", #b'!B318'
    ButtonPacket.BUTTON_4: "4", #b'!B417'
    ButtonPacket.UP: "UP",      #b'!B516'
    ButtonPacket.DOWN: "DOWN",  #b'!B615'
    ButtonPacket.LEFT: "LEFT",  #b'!B714'
    ButtonPacket.RIGHT: "RIGHT",#b'!B813'
}

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

def setup(name):
    ble.stop_advertising()
    ble.name = name

def connect():
    ble.start_advertising(advertisement)
    while not ble.connected:
        time.sleep(0.1)
        pass
    # Now we're connected
    print("Connected!")
    
def disconnect():
    for connection in ble.connections:
        connection.disconnect()
    print("Disconnected From all Devices")
    ble.stop_advertising()
    time.sleep(10)
    ble.start_advertising(advertisement)

def advertising():
    return ble.advertising

def start_advertising():
    if not ble.advertising:
        ble.start_advertising(advertisement, interval=0.5)

def connected():
    return ble.connected

def write(msg, newline=True):
    if newline:
        msg += "\n"
    uart.write(msg.encode())
    
def read(in_wait):
    return uart.read(in_wait)
    
def in_waiting():
    return uart.in_waiting

def button_press(data):
    packet = Packet.from_stream(io.BytesIO(data))
    if isinstance(packet, ButtonPacket) and packet.pressed:
        packet = Packet.from_stream(io.BytesIO(data))
        if packet.button in button_map:
            # print(f"{button_map[packet.button]} button pressed!, {data}")
            return button_map[packet.button]

    return None