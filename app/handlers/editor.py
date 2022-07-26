
from app.helper.message import MESSAGE, edit_message_text, remove_kb, get_info
from app.helper.keyboards import main_kb, sec1_kb, sec2_kb
from app.helper.download import delete_tmpdir, download_image, download_audio
from dispatcher import dp

from aiogram import types
from aiogram.types import ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class MusicInfo(StatesGroup):
    main = State()
    title = State()
    artist = State()
    thumb = State()


@dp.message_handler(content_types=[ContentType.AUDIO, ContentType.VOICE], state='*')
async def init_state(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await remove_kb(user_data.get('main_msg'))
    await state.finish()

    mf = message['audio'] or message['voice']
    if mf is None:
        return await message.answer(MESSAGE['error'])
    
    await state.update_data(
        file_id=mf.file_id,
        title=None,
        artist=None,
        thumb=None
    )

    if 'title' in mf:
        await state.update_data(title=mf.title)
    
    if 'performer' in mf:
        await state.update_data(artist=mf.performer)
    
    if 'thumb' in mf:
        await state.update_data(thumb=mf.thumb.file_id)

    user_data = await state.get_data()
    msg = MESSAGE['main'].format(
        *get_info(user_data, 'title', 'artist', 'thumb')
    )

    img_id = user_data.get('thumb')
    if img_id:
        tmpdir, img = await download_image(img_id)
        main_msg = await message.answer_photo(photo=img, caption=msg, reply_markup=main_kb)
        delete_tmpdir(tmpdir)
    else:
        main_msg = await message.answer(msg, reply_markup=main_kb)
    
    await state.update_data(main_msg=main_msg)
    await MusicInfo.main.set()


# ===== TITLE =====
@dp.callback_query_handler(lambda c: c.data == 'title', state=MusicInfo.main)
async def title_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    msg = MESSAGE['sec'].format(
        'Title',
        *get_info(user_data, 'title')
    )

    main_msg = await edit_message_text(user_data.get('main_msg'), msg, sec1_kb)
    await state.update_data(main_msg=main_msg)
    await MusicInfo.title.set()


@dp.message_handler(content_types=[ContentType.TEXT], state=MusicInfo.title)
async def title_handler(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    
    user_data = await state.get_data()
    msg = MESSAGE['imain'].format(
        'Gotcha!',
        *get_info(user_data, 'title', 'artist', 'thumb')
    )

    await message.delete()
    main_msg = await edit_message_text(user_data.get('main_msg'), msg, main_kb)
    await state.update_data(main_msg=main_msg)
    await MusicInfo.main.set()


@dp.message_handler(content_types=[ContentType.ANY], state=MusicInfo.title)
async def title_error(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    msg = MESSAGE['isec'].format(
        'Invalid option!',
        'Title',
        *get_info(user_data, 'title')
    )

    await message.delete()
    main_msg = await edit_message_text(user_data.get('main_msg'), msg, sec1_kb)
    await state.update_data(main_msg=main_msg)

# ===== ARTIST =====
@dp.callback_query_handler(lambda c: c.data == 'artist', state=MusicInfo.main)
async def artist_callback(callback_query: types.CallbackQuery, state: FSMContext):    
    user_data = await state.get_data()
    msg = MESSAGE['sec'].format(
        'Artist',
        *get_info(user_data, 'artist')
    )

    main_msg = await edit_message_text(user_data.get('main_msg'), msg, sec1_kb)
    await state.update_data(main_msg=main_msg)
    await MusicInfo.artist.set()


@dp.message_handler(content_types=[ContentType.TEXT], state=MusicInfo.artist)
async def artist_handler(message: types.Message, state: FSMContext):
    await state.update_data(artist=message.text)
    
    user_data = await state.get_data()
    msg = MESSAGE['imain'].format(
        'Gotcha!',
        *get_info(user_data, 'title', 'artist', 'thumb')
    )
    await message.delete()
    main_msg = await edit_message_text(user_data.get('main_msg'), msg, main_kb)
    await state.update_data(main_msg=main_msg)
    await MusicInfo.main.set()


@dp.message_handler(content_types=[ContentType.ANY], state=MusicInfo.artist)
async def artist_error(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    msg = MESSAGE['isec'].format(
        'Invalid option!',
        'Artist',
        *get_info(user_data, 'artist')
    )

    await message.delete()
    main_msg = await edit_message_text(user_data.get('main_msg'), msg, sec1_kb)
    await state.update_data(main_msg=main_msg)


# ===== THUMB =====
@dp.callback_query_handler(lambda c: c.data == 'thumb', state=MusicInfo.main)
async def thumb_callback(callback_query: types.CallbackQuery, state: FSMContext):    
    user_data = await state.get_data()
    msg = MESSAGE['sec'].format(
        'Thumb',
        *get_info(user_data, 'thumb')
    )

    main_msg = user_data.get('main_msg')
    kb = (sec2_kb if main_msg.photo else sec1_kb)

    main_msg = await edit_message_text(main_msg, msg, kb)
    await state.update_data(main_msg=main_msg)
    await MusicInfo.thumb.set()


@dp.message_handler(content_types=[ContentType.PHOTO], state=MusicInfo.thumb)
async def thumb_handler(message: types.Message, state: FSMContext):
    await state.update_data(thumb=message.photo[1].file_id)
    
    user_data = await state.get_data()
    msg = MESSAGE['imain'].format(
        'Gotcha!',
        *get_info(user_data, 'title', 'artist', 'thumb')
    )
    tmpdir, img = await download_image(user_data.get('thumb'))

    main_msg = user_data.get('main_msg')
    await main_msg.delete()
    
    main_msg = await message.answer_photo(photo=img, caption=msg, reply_markup=main_kb)
    await state.update_data(main_msg=main_msg)

    delete_tmpdir(tmpdir)
    await message.delete()
    await MusicInfo.main.set()


@dp.message_handler(content_types=[ContentType.ANY], state=MusicInfo.thumb)
async def thumb_error(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    msg = MESSAGE['isec'].format(
        'Invalid option!',
        'Thumb',
        *get_info(user_data, 'thumb')
    ) 

    main_msg = user_data.get('main_msg')
    kb = (sec2_kb if main_msg.photo else sec1_kb)

    main_msg = await edit_message_text(main_msg, msg, kb)
    await state.update_data(main_msg=main_msg)
    await message.delete()


@dp.callback_query_handler(lambda c: c.data == 'delete', state=MusicInfo.thumb)
async def thumb_delete_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(thumb=None)
    
    user_data = await state.get_data()
    msg = MESSAGE['imain'].format(
        'Gotcha!',
        *get_info(user_data, 'title', 'artist', 'thumb')
    )

    main_msg = user_data.get('main_msg')
    await main_msg.delete()
    
    main_msg = await callback_query.message.answer(msg, reply_markup=main_kb)
    await state.update_data(main_msg=main_msg)
    await MusicInfo.main.set()


# ===== BACK =====
@dp.callback_query_handler(lambda c: c.data == 'back', state=[MusicInfo.title, MusicInfo.artist, MusicInfo.thumb])
async def back_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    msg = MESSAGE['main'].format(
        *get_info(user_data, 'title', 'artist', 'thumb')
    )

    main_msg = await edit_message_text(user_data.get('main_msg'), msg, main_kb)
    await state.update_data(main_msg=main_msg)
    await MusicInfo.main.set()


# ===== DOWNLOAD =====
@dp.callback_query_handler(lambda c: c.data == 'download', state=MusicInfo.main)
async def download_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    main_msg = user_data.get('main_msg')

    if user_data.get('title') is None:
        msg = MESSAGE['imain'].format(
            'No Title! Give it a title first',
            *get_info(user_data, 'title', 'artist', 'thumb')
        )
        main_msg = await edit_message_text(main_msg, msg, reply_markup=main_kb)
        return await state.update_data(main_msg=main_msg)

    if user_data.get('artist') is None:
        msg = MESSAGE['imain'].format(
            'No Artist! Give it a Artist first',
            *get_info(user_data, 'title', 'artist', 'thumb')
        )
        main_msg = await edit_message_text(main_msg, msg, reply_markup=main_kb)
        return await state.update_data(main_msg=main_msg)


    await remove_kb(main_msg)
    await callback_query.answer('Processing, please wait')    

    tmpdir1, audio, duration = await download_audio(user_data.get('file_id'))
    tmpdir2, thumb = await download_image(user_data.get('thumb'))

    await callback_query.message.answer_audio(
        audio=audio,
        title=user_data.get('title', 'cool song'),
        performer=user_data.get('artist', 'cool artist'),
        thumb=thumb,
        duration=duration
    )

    delete_tmpdir(tmpdir1, tmpdir2)
    await state.finish()


# ===== INCORRECT INPUT HANDLER =====
@dp.message_handler(content_types=[ContentType.ANY], state=MusicInfo.main)
async def incorect_music_input_handler(message: types.Message, state: FSMContext):
    await message.delete()

    user_data = await state.get_data()
    msg = MESSAGE['imain'].format(
        'Choose one of the options below',
        *get_info(user_data, 'title', 'artist', 'thumb')
    )

    main_msg = await edit_message_text(user_data.get('main_msg'), msg, reply_markup=main_kb)
    await state.update_data(main_msg=main_msg)
