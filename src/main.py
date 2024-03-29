from interstate75 import Interstate75
import CONFIG
import logging
import machine
import network
import tfl
import time
import uasyncio as asyncio

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


def flash_hello_world():
    i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
    graphics = i75.display

    MAGENTA = graphics.create_pen(255, 0, 255)
    BLACK = graphics.create_pen(0, 0, 0)
    WHITE = graphics.create_pen(255, 255, 255)

    while True:
        graphics.set_pen(MAGENTA)
        graphics.text("hello", 1, 0, scale=1)
        graphics.set_pen(WHITE)
        graphics.text("world", 1, 6, scale=1)
        i75.update(graphics)
        time.sleep(0.5)

        graphics.set_pen(BLACK)
        graphics.clear()
        i75.update(graphics)
        time.sleep(0.5)


async def main():
    logging.basicConfig(level=logging.DEBUG)

    connect_wlan(CONFIG.SSID, CONFIG.PSK)
    # flash_hello_world()

    logging.info(await tfl.route_to_brit())


asyncio.run(main())
