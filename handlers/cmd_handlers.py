from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from utils.database import Database
from config import DB_NAME
from keyboards.reg_keyboards import kb_register
db = Database(DB_NAME)


cmd_router = Router()


@cmd_router.message(CommandStart())
async def cmd_start(message: Message):
    users = db.get_user(message.from_user.id)
    if not users:
        msg = message.from_user
        db.add_new_user(msg.id, msg.username, msg.first_name, msg.last_name)
        print("new user inserted")
        await message.answer(text="Iltimos ro'yxatdan o'ting!", reply_markup=kb_register)
    elif not users[6]:
        await message.answer(text="Iltimos ro'yxatdan o'ting!", reply_markup=kb_register)
    else:
        await message.answer(f"Hurmatli {users[5]}, qaytganingiz bilan!")
