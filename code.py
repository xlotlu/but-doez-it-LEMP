import asyncio
#from lemp import Lemp
from colorwheel_lemp import ColorWheelLemp


if __name__ == "__main__":
    #does_it = Lemp()
    does_it = ColorWheelLemp()
    asyncio.run(does_it.lemp())
