import asyncio
from lemp import Lemp


if __name__ == "__main__":
    does_it = Lemp()
    asyncio.run(does_it.lemp())
