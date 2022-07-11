#!venv/bin/python
import logging

import add_to_bd
import add_to_fs

from aiogram import Bot, Dispatcher, executor, types
from os import getenv, remove
from sys import exit


# Получаем api_token из Environment Variables
_API_TOKEN = getenv("API_TOKEN")
if not _API_TOKEN:
    exit("Error: no token provided")

# Настраиваем логирование

# Если хотите создать файл с логами - используйте имя файла в basicConfig()
# Пример: filename='project_log.log'

logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчера
bot = Bot(token=_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Этот хендлер вызывается когда пользователь отправляет `/start'
    """
    # Добавляем данные пользователя в таблицу
    await add_to_bd.db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name,
                                 user_surname=message.from_user.last_name, username=message.from_user.username)

    await message.answer(f"Привет, {message.from_user.first_name}!\nЯ HTR_Bot!")


# Типы содержимого тоже можно указывать по-разному.
@dp.message_handler(content_types=['photo'])
async def download_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await add_to_bd.update_photo_number(user_id=message.from_user.id)

    photo_number = await add_to_bd.get_photo_number(message.from_user.id)

    await bot.download_file(file_path, f"tmp\\{message.from_user.id}.jpg")

    await add_to_fs.upload_file(object_name=f"tmp\\{message.from_user.id}.jpg", bucket_name=getenv("BUCKET_NAME"),
                                object_bucket_name=f"{message.from_user.id}/{photo_number}.jpg")

    remove(f"tmp\\{message.from_user.id}.jpg")

    # Убедитесь, что каталог /tmp/somedir существует!
    # Используем индекс [-1], чтобы взять большее по размеру изображение
    # await message.photo[-1].download(destination_dir=f'tmp\\{message.from_user.id}')


if __name__ == "__main__":
    """
    long polling - поддерживает постоянное подключение к серверу
    """
    # чтобы избежать ошибки 'Updates were skipped successfully' - удалите 'skip_updates=True'
    executor.start_polling(dp, skip_updates=True)
