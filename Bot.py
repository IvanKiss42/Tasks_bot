from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import DatBase
from config import TOKEN

db = DatBase()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class task(StatesGroup):
    waiting_for_task_description = State()
    waiting_for_delete_task_description = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(
        'Добрый день! Это бот который помогает вести список задач',
        reply_markup=pool_button
    )


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(
        'Если Вы хоите добавить задачу нажмите на кнопку "tsk",\n'
        'Если Вы вывести список дел нажмите на кнопку "list"',
        reply_markup=pool_button
    )


@dp.message_handler(commands=['add'], state='*')
async def new_task(message: types.Message, state: FSMContext):
    await message.answer('Опишите задачу', reply_markup=None)
    await state.set_state(task.waiting_for_task_description.state)


@dp.message_handler(state=task.waiting_for_task_description.state)
async def task_description(message: types.Message, state: FSMContext):
    await state.update_data(redact=message.text)
    user_data = await state.get_data()
    data = user_data['redact']
    await message.answer(f'Добавлена задача {data}')
    db.add_task(data)
    await state.finish()


@dp.message_handler(commands=['tsk'], state='*')
async def task_list(message: types.Message):
    msg = 'Список задач: \n'
    tasks_list = db.list_tasks()
    for task in tasks_list:
        msg += ' - ' + task[0] + ' \n'
    await message.answer(msg)


@dp.message_handler(commands=['delete'], state='*')
async def delete_task(message: types.Message, state: FSMContext):
    await message.answer(
        'Описание какой задачи надо удалить?'
    )
    await state.set_state(task.waiting_for_delete_task_description.state)


@dp.message_handler(state=task.waiting_for_delete_task_description.state)
async def delete_task_description(message: types.Message, state: FSMContext):
    await state.update_data(redact=message.text)
    user_data = await state.get_data()
    description = user_data['redact']
    if not db.check_task(description):
        await message.answer(
            f'{"Не существует такой задачии, "}'
            f'введите описание задачи снова'
        )
        return
    db.remove_task(description)
    await message.answer(f'Удалена задача "{description}"')
    await state.finish()

registration_button = KeyboardButton('/add')
checking_button = KeyboardButton('/tsk')
remove_button = KeyboardButton('/delete')

pool_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(registration_button).add(checking_button).add(remove_button)

if __name__ == '__main__':
    db.create_tasks_table()
    executor.start_polling(dp, skip_updates=True)
