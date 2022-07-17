
from app.helper.message import remove_kb

from aiogram import types
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from dispatcher import dp


@dp.message_handler(content_types=[ContentType.ANY], state='*')
async def second_state_check(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await remove_kb(user_data.get('main_msg'))

    await state.finish()
    await message.answer('Please, send / forward me an audio / voice message')


@dp.callback_query_handler(state='*')
async def thumb_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.answer('Error: old message')

    await remove_kb(callback_query.message)
