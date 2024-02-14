import sys

from aiogram import Bot, Dispatcher
import asyncio
import logging
from aiogram.enums import ParseMode
from config import BPT_TOKEN
from handlers.cmd_handlers import cmd_router
from handlers.reg_handlers import reg_router
from handlers.msg_handlers import msg_router


async def main():
    bot = Bot(BPT_TOKEN, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    db = Dispatcher()
    db.include_routers(msg_router, cmd_router, reg_router)
    await db.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot stopped")
