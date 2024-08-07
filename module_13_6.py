from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from mailbox import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


aip='gkljrtljtlgjflj5656565ghhf     fgfgfgf'#Ромдомные токены, не используйте их в реальной работе
bot=Bot(token=aip)
dp=Dispatcher(bot,storage= MemoryStorage())

kb=InlineKeyboardMarkup()
button=InlineKeyboardButton(text='Рассчитать', callback_data='calculate')
kb.add(button)


start_kb=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать норму калорий'),KeyboardButton(text='Формулы расчёта')]],
                             resize_keyboard=True)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=['start','/start'])
async  def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb )




@dp.callback_query_handler(text='calculate')
async def get_formulas(call):
    await call.message.answer(f'Выберите опцию:', reply_markup=start_kb )
    await call.answer()



@dp.message_handler(text=['Формулы расчёта'])
async def inf1(message):
    await message .answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')




@dp.message_handler(text=['Рассчитать норму калорий'])
async def set_age(message):
        await message.answer('Введите ваш возраст:')
        await UserState.age.set()

# @dp.message_handler(text=['Информация','/info'])
# async def info(message):
#     await message.answer('Информация о боте:')
#     await message.answer('Команда /start - начало работы с ботом')
#     await message.answer('Команда /info - получение информации о боте')
#     await message.answer('Команда /calories - начало рассчета калорий')
#
#

@dp.message_handler(state=UserState.age)
async def set_growth(message,state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите ваш рост:')
    print(f'мы сохранили {message.text}')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=float(message.text))
    await message.answer('Введите ваш вес:')
    print(f'мы сохранили {message.text}')
    await UserState.weight.set()



@dp.message_handler(state=UserState.weight)
async def send_calories(message,state):
    print(f'мы сохранили {message.text}')
    await state.update_data(weight=float(message.text))
    data= await state.get_data()
    # Simplified Mifflin - St Jeor formula for calorie calculation (example for women)
    calories = 655 + (9.6 * data['weight']) + (1.8 * data['growth']) - (4.7 * data['age'])
    await message.answer(f'Ваша максимальная норма калорий: {calories}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)