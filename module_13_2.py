# Домашнее задание по теме "Хендлеры обработки сообщений".
# Задача "Бот поддержки (Начало)".

import hashlib
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
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
    print("Привет! Я бот помогающий твоему здоровью.")
    await message.reply("Привет! Я - бот,  помогающий твоему здоровью.")  # Отправляем ответ пользователю

@dp.message_handler()
async def all_messages(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.reply("Введите команду /start, чтобы начать общение.")  # Отправляем ответ пользователю

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)