# https://github.com/PopovGP/picodebug/tree/main

from machine import RTC
from time import sleep


def logPrint(
    myParam,
    outputToConsole=True,
    outputToFile=True,
    makeTimeStamp=True,
    led=None,
    numberOfBlinks=0,
):
    if outputToConsole:
        print(f"{RTC().datetime()} - {myParam}")
    if outputToFile:
        with open("log1.txt", "ab") as f:
            if makeTimeStamp:
                f.write(f"{RTC().datetime()} - {myParam}\n")
            else:
                f.write(f"{myParam}\n")
    if numberOfBlinks > 0:
        count = 0
        while count < numberOfBlinks:
            count = count + 1
            led.on()
            sleep(0.3)
            led.off()
            sleep(0.1)


def logClean():
    import os

    maxFiles = 8

    for i in range(maxFiles):
        try:
            os.remove(f"log{i+1}.txt")
        except:
            pass


def logRotate():
    import os

    fileSize = 0
    maxSize = 100000
    maxFiles = 8

    try:
        fileSize = os.stat("log1.txt")[6]

        # We should do rotation
        if fileSize >= maxSize:
            # Remove last file and free space
            try:
                os.remove(f"log{maxFiles}.txt")

            except:
                pass

            # Shift files
            for i in range(maxFiles - 1, 0, -1):
                try:
                    os.rename(f"log{i}.txt", f"log{i+1}.txt")

                except:
                    pass
    except:
        pass
