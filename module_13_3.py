# Домашнее задание по теме "Хендлеры обработки сообщений".
# Задача "Он мне ответил"!

import hashlib
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import API_TOKEN  # Импортируем токен из модуля config

# Хеширование токена
def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()

hashed_api = hash_token(API_TOKEN)
print(f"Строка токена после хеширования: {hashed_api}")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start(message):
    # Отправляем сообщение пользователю в чат
    await message.answer("Привет! Я - бот, помогающий твоему здоровью.")  # Асинхронный ответ пользователю

@dp.message_handler()
async def all_messages(message):
    # Отправляем сообщение пользователю, если он не использует команду /start
    await message.answer("Введите команду /start, чтобы начать общение.")  # Асинхронный ответ пользователю

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)