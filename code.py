import asyncio
#from rgb_channel_mode import RGBChannelMode
from rgb_colorwheel_mode import RGBColorWheelMode


if __name__ == "__main__":
    #does_it = RGBChannelMode()
    does_it = RGBColorWheelMode()
    asyncio.run(does_it.lemp())
