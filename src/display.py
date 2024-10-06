from interstate75 import Interstate75
import logging
import time


def flash_hello_world():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("getting i75...")
    i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
    logging.debug("getting display...")
    graphics = i75.display

    logging.debug("getting pens...")
    MAGENTA = graphics.create_pen(255, 0, 255)
    BLACK = graphics.create_pen(0, 0, 0)
    WHITE = graphics.create_pen(255, 255, 255)

    while True:
        logging.debug("about to write hello world...")
        graphics.set_pen(MAGENTA)
        graphics.text("hello", 1, 0, scale=1)
        graphics.set_pen(WHITE)
        graphics.text("world", 1, 6, scale=1)
        i75.update(graphics)
        time.sleep(0.5)

        logging.debug("about to clear display...")
        graphics.set_pen(BLACK)
        graphics.clear()
        i75.update(graphics)
        time.sleep(0.5)


# scroll through journey info one time
def scroll_bus_journey_status(
    route: str,
    origin: str,
    destination: str,
    deps_and_arrs: list[(str, str)],
    line_status: int,
    disruptions: str,
):

    i75 = Interstate75(display=Interstate75.DISPLAY_INTERSTATE75_64X32)
    graphics = i75.display

    if line_status == 10:
        pen = graphics.create_pen(0, 255, 0)  # green
    elif line_status < 5:
        pen = graphics.create_pen(255, 0, 0)  # red
    else:
        pen = graphics.create_pen(255, 191, 0)  # amber

    graphics.set_pen(pen)
    graphics.text(destination, 1, 0, scale=1)
