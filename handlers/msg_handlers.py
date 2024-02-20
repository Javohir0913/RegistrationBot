from aiogram import F, Router
from aiogram.types import Message, FSInputFile, InputMediaPhoto
import pdfkit
import os
import fitz
from PIL import Image

from utils.database import Database
from config import DB_NAME


db = Database(DB_NAME)
msg_router = Router()



@msg_router.message(F.document)
async def file_ot_jpg(message: Message):
    user = db.get_user(message.from_user.id)
    if user[8] < 444:
        file = await message.bot.get_file(file_id=message.document.file_id)
        output_fayl = "C:\\Users\\Victus\\Desktop\\python\\5-oy\\lesson_10_re_tg_bot\\downloads\\"
        file_path = file.file_path
        await message.bot.download_file(file_path, f"{output_fayl}{message.document.file_name}")
        convert_pdf_to_images(f"{output_fayl}{message.document.file_name}", output_fayl, message.document.file_name)
        os.remove(path=output_fayl + message.document.file_name)
        my_albom = []
        for i in os.listdir(path=output_fayl):
            my_albom.append(InputMediaPhoto(media=FSInputFile(f"{output_fayl}{i}")))
        await message.bot.send_media_group(chat_id=message.from_user.id,
                                           media=my_albom)
        for i in os.listdir(path=output_fayl):
            os.remove(output_fayl+i)
    else:
        await message.answer("urunishlaringiz tugagan")


@msg_router.message(F.text[0:6] == "https:")
async def url_message(message: Message):
    user = db.get_user(message.from_user.id)
    if user[8] < 443:
        url = message.text
        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        output_fayl = "C:\\Users\\Victus\\Desktop\\python\\5-oy\\lesson_10_re_tg_bot\\downloads\\"
        pdfkit.from_url(url, output_fayl + "fayl.pdf",
                        configuration=config)
        await message.answer("yuklab olish boshlandi")
        await message.reply_document(document=FSInputFile(path=output_fayl+"fayl.pdf", filename="file.pdf"))
        os.remove(path=output_fayl + "fayl.pdf")
        db.up_url(message.from_user.id)
    else:
        await message.answer("urunishlaringiz tugagan")


def convert_pdf_to_images(pdf_path, output_folder, pdf_file):
    pdf_document = fitz.open(pdf_path)
    num_pages = pdf_document.page_count
    print(f"{pdf_path} ichida: {num_pages} sahifa")
    for page_number in range(num_pages):
        page = pdf_document.load_page(page_number)
        image_list = page.get_pixmap()
        image = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)
        image.save(os.path.join(output_folder, f"{pdf_file.replace(".pdf", "")}_page_{page_number + 1}.jpg"))
    pdf_document.close()