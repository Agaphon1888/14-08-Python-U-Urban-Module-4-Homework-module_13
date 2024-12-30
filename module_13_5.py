# Домашнее задание по теме "Клавиатура кнопок".
# Задача "Меньше текста, больше кликов".

import hashlib
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import API_TOKEN  # Импортируем токен из модуля config


# Хеширование токена
def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()


hashed_api = hash_token(API_TOKEN)
print(f"Строка токена после хеширования: {hashed_api}")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Определяем состояния пользователя
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()

# Создание клавиатуры
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
btn_calculate = KeyboardButton('Рассчитать')
btn_info = KeyboardButton('Информация')
keyboard.add(btn_calculate, btn_info)

@dp.message_handler(commands=['start'])
async def start(message):
    # Отправляем сообщение пользователю и клавиатуру в чат
    await message.answer("Привет! Я - бот, помогающий твоему здоровью.", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == 'Рассчитать')
async def set_age(message):
    await UserState.age.set()  # Устанавливаем состояние
    await message.answer("Введите свой возраст:")

@dp.message_handler(state=UserState.age)
async def set_growth(message: str, state: FSMContext):
    await state.update_data(age=message.text)  # Обновляем состояние
    await UserState.growth.set()  # Устанавливаем следующее состояние
    await message.answer("Введите свой рост в сантиметрах:")

@dp.message_handler(state=UserState.growth)
async def set_weight(message: str, state: FSMContext):
    await state.update_data(growth=message.text)  # Обновляем состояние
    await UserState.weight.set()  # Устанавливаем следующее состояние
    await message.answer("Введите свой вес в килограммах:")

@dp.message_handler(state=UserState.weight)
async def set_gender(message: str, state: FSMContext):
    await state.update_data(weight=message.text)  # Обновляем состояние
    await UserState.gender.set()  # Устанавливаем следующее состояние
    await message.answer("Введите свой пол (М или Ж):")

@dp.message_handler(state=UserState.gender)
async def send_calories(message: str, state: FSMContext):
    user_data = await state.get_data()  # Получаем данные состояния
    age = int(user_data.get('age'))
    growth = int(user_data.get('growth'))
    weight = int(user_data.get('weight'))
    gender = message.text.strip().upper()  # Приводим к верхнему регистру

    # Вычисляем норму калорий в зависимости от пола
    if gender == "М":
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
    elif gender == "Ж":
        calories = 10 * weight + 6.25 * growth - 5 * age - 161
    else:
        await message.answer("Некорректный ввод. Пожалуйста, введите 'М' или 'Ж'.")
        return

    await message.answer(f"Ваша норма калорий: {calories} калорий в день.")

    # Завершаем состояние
    await state.finish()

@dp.message_handler(lambda message: message.text == 'Информация')
async def info(message):
    await message.answer("Это бот для расчёта вашей нормы калорий. Нажмите 'Рассчитать', чтобы начать!")

@dp.message_handler()
async def all_messages(message):
    await message.answer("Пожалуйста, воспользуйтесь кнопками ниже.", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)