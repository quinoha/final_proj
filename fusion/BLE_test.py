import numpy as np
import csv
import asyncio

from bleak import BleakScanner, BleakClient

'''
BLE Connection between Raspberry-Pi 5 and ESP-32
Used library: Bleak, Github link: https://github.com/hbldh/bleak/tree/develop 
Reference article: https://randomnerdtutorials.com/ble-raspberry-pi-and-pi-pico-w/ 
 
    Central Device: Raspberry Pi
    Peripheral Device: ESP-32
    
1. BLE Peripheral advertises its existence.
2. BLE Central Device scans for BLE devices.
3. Central Device finds the peripheral and connects to it.
4. It reads GATT profile and searches for service.
5. Interact with Central device (read data)
'''


# received BPM data will be saved as .csv
FILE_NAME = "workout_bpm.csv"

# Run scanner to discover ESP-32
async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"Name: {d.name}, address: {d.adreess}")

asyncio.run(run())

# TODO: add notification handler to receive data.
def notification_handler(sender, data):
    
    value = int.from_
    
    
    pass

async def main(address):
    async with BleakClient(address) as client:
        print(f"Connected to BLE address: {address}")


# TODO: test main code
    
    