from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import asyncio
from config import API_KEY
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
bt_1 = KeyboardButton('Рассчитать')
bt_2 = KeyboardButton('Информация')
kb.row(bt_1, bt_2)

@dp.message_handler(text='Рассчитать')
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = (10 * int(data['weight'])) + (6.25 * int(data['growth'])) - (5 * int(data['age'])) + 5
    print(data)
    await message.answer(f'Ваша норма калорий {calories}')
    await state.finish()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


# kb = ReplyKeyboardMarkup(resize_keyboard=True)
# button = KeyboardButton(text='Информация')
# button2 = KeyboardButton(text='Начало')
# kb.add(button)
# kb.add(button2)
#
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.answer('Hello', reply_markup=kb)
#
# @dp.message_handler(text='Информация')
# async def inform(message: types.Message):
#     await message.answer('Информация о Боте')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
