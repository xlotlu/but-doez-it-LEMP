import asyncio
#from lemp import RGBChannelMode
from colorwheel_lemp import RGBColorWheelMode


if __name__ == "__main__":
    #does_it = RGBChannelMode()
    does_it = RGBColorWheelMode()
    asyncio.run(does_it.lemp())
