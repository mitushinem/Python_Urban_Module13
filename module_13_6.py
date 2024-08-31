from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import asyncio
from config import API_KEY
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

kb_inline = InlineKeyboardMarkup()
bt_ln_1 = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
bt_ln_2 = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
kb_inline.add(bt_ln_1, bt_ln_2)


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=kb_inline)



@dp.callback_query_handler(lambda query: query.data == 'formulas')
async def get_formulas(query: types.CallbackQuery):
    await query.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await query.message.answer('для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await query.answer()


@dp.callback_query_handler(lambda query: query.data == 'calories')
async def set_age(query: types.CallbackQuery):
    await query.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await query.answer()


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
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb_inline)


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


# kb = InlineKeyboardMarkup()
# button = InlineKeyboardButton(text='Информация', callback_data='info')
# kb.add(button)
#
# start_menu = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text='Info')],
#         [
#             KeyboardButton(text='shop'),
#             KeyboardButton(text='donate')
#         ]
#     ],
#     resize_keyboard=True
# )
#
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.answer('Рады вас видеть', reply_markup=kb)
#
#
# @dp.callback_query_handler(lambda query: query.data == 'info')
# async def info(query: types.CallbackQuery):
#     await query.message.answer('Информация о боте')
#     await query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
