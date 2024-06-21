from datetime import datetime
from config import dp
from dbmethods import *
from random import randint
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from aiogram import types
from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon_ru import LEXICON_COMMANDS_RU

# Объявляем стейты
class States(StatesGroup):
    fullname = State()
    delays_number = State()
    passes_number = State()
    choice = State()

def gen_random():
    return randint(1, 9999999)

iduser = None

def se(value):
    global iduser
    iduser = value

def ge():
    global iduser
    print (iduser)
    return iduser

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS_RU.items()
    ]
    await bot.set_my_commands(main_menu_commands)

# Команды Бота
@dp.message(Command('start'))
async def start_handle(message: types.Message):
    print(message.from_user.id)
    print(message.from_user.username)
    await message.answer('Привет!\nЭто чат бот по онлайн рапортичке\nВсе функции можно узнать по команде\n /help')

@dp.message(Command('help'))
async def handle(message: types.Message):
    await message.answer('''
/addstud – Добавить студента в список
/list – Просмотреть список студентов
/del – Удалить студента из списка (Введите команду и через пробел ФИО студента)
/rep – Создать отчёт
/m - Отметить отсутствие или опоздание студента (Введите команду и через пробел ФИО студента)
''')


@dp.message(Command('rep'))
async def handle(message: types.Message):
    num = gen_random()
    rep(num)
    file = FSInputFile(f'{num}.xlsx')
    await message.answer_document(file)


@dp.message(Command('addstud'))
async def handle(message: types.Message, state: FSMContext):
    await message.answer('Введите ФИО:')
    await state.set_state(States.fullname)


@dp.message(States.fullname)
async def handle(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer('Введите количество опозданий:')
    await state.set_state(States.delays_number)


@dp.message(States.delays_number)
async def handle(message: types.Message, state: FSMContext):
    await state.update_data(delays_number=message.text)
    await message.answer('Введите количество пропусков:')
    await state.set_state(States.passes_number)


@dp.message(States.passes_number)
async def handle(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    fullname = data['fullname']
    delays_number = data['delays_number']
    passes_number = message.text
    date = datetime.today()
    put(user_id, fullname, delays_number, passes_number, date)
    await message.answer(f'Студент {fullname} добавлен')
    await state.clear()


@dp.message(Command('list'))
async def handle(message: types.Message):
    fullnames = fetchall()
    text = ''
    for fullname in fullnames:
        text += fullname[0] + '\n'
    await message.answer(text)


@dp.message(Command('del'))
async def handle(message: types.Message):
    fullname = message.text[5:]
    print(len(fullname))
    delete(fullname)
    await message.answer(f'Студент {fullname} удален')


@dp.message(Command('m'))
async def handle(message: types.Message, state: FSMContext):
    fullname = message.text[3:]
    await state.update_data(fullname=fullname)
    await message.answer('опоздал или пропустил?')
    await state.set_state(States.choice)


@dp.message(States.choice)
async def handle(message: types.Message, state: FSMContext):
    data = await state.get_data()
    fullname = data['fullname']
    choice = message.text.lower()
    mark(fullname, choice)
    await message.answer('Записано')
    await state.clear()
