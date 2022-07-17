
from app.helper.message import remove_kb

from aiogram import types
from aiogram.dispatcher import FSMContext
from dispatcher import dp


@dp.message_handler(commands=['start', 'help'], state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await remove_kb(user_data.get('main_msg'))

    await state.finish()
    await message.answer('Hi! Send / forward me an audio / voice message')


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await remove_kb(user_data.get('main_msg'))
    
    await state.finish()
    await message.answer('Action canceled')
