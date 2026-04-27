import numpy as np
from bleak import BleakScanner

async def run():
    devices = await BleakScanner.discover()
    for d in devices
    print(f"Name: {d.name}, address: {d.adreess}")

asyncio.run(run())

