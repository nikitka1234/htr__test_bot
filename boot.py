#!venv/bin/python
import logging
from add_to_bd import db_table_val
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit


# getting the api_token from Environment Variables
_API_TOKEN = getenv("API_TOKEN")
if not _API_TOKEN:
    exit("Error: no token provided")

# Configure logging

# if u wanna create a file with logs - use filename in basicConfig()
# Sample: filename='project_log.log'

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start' command
    """
    # добавляем данные пользователя в таблицу
    db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name,
                 user_surname=message.from_user.last_name, username=message.from_user.username)

    await message.answer(f"Hi, {message.from_user.first_name}!\nI'm HTR_Bot!\nPowered by aiogram.")


@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def download_doc(message: types.Message):
    # Скачивание в каталог с ботом с созданием подкаталогов по типу файла
    if '.pdf' in message:
        await message.document.download(destination_dir='tmp')


# Типы содержимого тоже можно указывать по-разному.
@dp.message_handler(content_types=['photo'])
async def download_photo(message: types.Message):
    # Убедитесь, что каталог /tmp/somedir существует!
    # Используем индекс [-1], чтобы взять большее по размеру изображение
    await message.photo[-1].download(destination_dir='tmp')


if __name__ == "__main__":
    """
    run long polling - support for a permanent connection to the server
    """
    # to exclude an error 'Updates were skipped successfully' - delete 'skip_updates=True'
    executor.start_polling(dp, skip_updates=True)
