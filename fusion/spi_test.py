import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0) # bus 0, device 0 (CE0)
spi.max_speed_hz = 100000 # 처음엔 100kHz로 안전하게 테스트!
spi.mode = 0 # CPOL=0, CPHA=0 (PMOD 표준)

try:
    while True:
        # 0xAA (10101010)를 KV260으로 쏘고, 결과를 받아옴
        resp = spi.xfer2([0xAA])
        print(f"KV260으로부터 받은 데이터: {resp[0]}")
        time.sleep(1)
finally:
    spi.close()