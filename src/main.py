import CONFIG
import logging
import network
import time
import tfl
import uasyncio as asyncio
import display

"""
1. WiFi ✅
2. TLF webservice
3. Rendering
4a. Tests? Pytest
4b. CI: Github -> CircleCI: https://realpython.com/python-continuous-integration/
5. Watchdog (restart on hang) (also on wlan disconnect)
6. Power supply (crimped wires)
7. Mount (frame)
"""


def connect_wlan(ssid, psk, timeout_secs=30):
    # https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)

    # Wait for connect or fail
    max_wait = timeout_secs
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        logging.debug(f"waiting for wlan connection to {ssid}...")
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError(f"network connection failed: {wlan.status}")
    else:
        status = wlan.ifconfig()
        logging.info(f"connected: ip={status[0]}")


async def main():
    logging.basicConfig(level=logging.DEBUG)

    connect_wlan(CONFIG.SSID, CONFIG.PSK)
    logging.info("connected to wifi, calling display...")

    brit = tfl.route_to_brit()
    logging.info(brit)

    while True:
        # await display_commute_info()
        logging.info(await tfl.route_to_brit())


asyncio.run(main())
