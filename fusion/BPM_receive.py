import numpy as np
import csv
import asyncio

from bleak import BleakClient

FILE_NAME = "workout_bpm.csv"
CHAR_UUID = ""


def notification_handler(sender, data):
    
    value = int.from_
    
    
    pass

async def main(address):
    # CSV file header
    
    
    # start BLE client mode and monitor
    async with BleakClient(address) as client:
        print(f"Connected to BLE address: {address}")
        
    
    