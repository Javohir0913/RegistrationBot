from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import F, Router
from config import DB_NAME
from keyboards.reg_keyboards import kb_request_contact
from states.reg_states import RegisterStates
from utils.database import Database
# from keyboards.reg_keyboards import

reg_router = Router()
db = Database(DB_NAME)


@reg_router.message(F.text == "Ro'yhatdan o'tish")
async def register_start(message: Message, state=FSMContext):
    users = db.get_user(message.from_user.id)
    if users[6]:
        await message.answer(
            f"Hurmatli {users[5]} siz tizimdan ro'yxatdan o'tgansiz",
            reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f"Ro'yhatdan o'tish jarayonini boshlaymiz\n"
                             f"Iltimos to'liq ism familyagizni krting:",
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterStates.regName)


@reg_router.message(RegisterStates.regName)
async def register_name(message:Message, state=FSMContext):
    await message.answer(f"Yaxshi {message.text}\nIltimos, email krting:")
    await state.update_data(regName=message.text)
    await state.set_state(RegisterStates.regEmail)


@reg_router.message(RegisterStates.regEmail)
async def register_email(message: Message, state=FSMContext):
    await state.update_data(reg_Email=message.text)
    await state.set_state(RegisterStates.regBirth_date)
    await message.answer("tug'ilgan kunigizni krting")


@reg_router.message(RegisterStates.regBirth_date)
async def register_regBirth_date(message:Message, state=FSMContext):
    await state.update_data(regBirth_date=message.text)
    await state.set_state(RegisterStates.regPhone)
    await message.answer("Telefon raqamingizni yuboring",reply_markup=kb_request_contact)


@reg_router.message(RegisterStates.regPhone)
async def register_phone(message: Message, state=FSMContext):
    try:
        await state.update_data(reg_phone=message.contact.phone_number)
        reg_date = await state.get_data()
        reg_name = reg_date.get("regName")
        reg_email = reg_date.get("reg_Email")
        reg_birth_date = reg_date.get("regBirth_date")
        reg_phone = reg_date.get("reg_phone")
        await message.answer(f"Hurmatli {reg_name} siz tizimdan muvaffaqiyatli ro'yxatdan o'tdingiz",
                      reply_markup=ReplyKeyboardRemove())
        db.update_user(message.from_user.id, reg_name, reg_phone, reg_email, reg_birth_date)
        await state.clear()
    except:
        await message.answer(f"Iltimos telefon raqamingizni yuboring")

