
import logging
import asyncio

import app
from dispatcher import dp

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    level=logging.INFO,
)


async def main():
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
