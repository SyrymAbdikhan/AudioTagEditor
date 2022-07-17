
import logging

from aiogram.utils.exceptions import MessageNotModified

MESSAGE = {
    'main': 'Title: {0}\nArtist: {1}\nThumb: {2}',
    'imain': '{0}\n\nTitle: {1}\nArtist: {2}\nThumb: {3}',
    'sec': '{0}: {1}\n\nSend me an audio {0}\nOr press one of the options below',
    'isec': '{0}\n\n{1}: {2}\n\nSend me an audio {1}\nOr press one of the options below',
    'error': 'Error: contact developer @Honey_Niisan',
}


def get_info(data, *info):
    result = []
    for el in info:
        if el == 'thumb':
            text = ('🖼' if data.get(el) else f'no {el}')
        else:
            text = (data.get(el) or f'no {el}')
        result.append(text)
    return result


def get_message_text(message):
    if message.photo:
        return message.caption
    
    return message.text


async def edit_message_text(message, text, reply_markup=None):
    try:
        if message.photo:
            return await message.edit_caption(text, reply_markup=reply_markup)
        return await message.edit_text(text, reply_markup=reply_markup)
    except MessageNotModified as e:
        logging.error(e)
        return message


async def remove_kb(message):
    if not message:
        return

    await edit_message_text(message, get_message_text(message))
