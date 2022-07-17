
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_kb = InlineKeyboardMarkup(row_width=1).row(
    InlineKeyboardButton('Title', callback_data='title'),
    InlineKeyboardButton('Artist', callback_data='artist'),
).row(
    InlineKeyboardButton('Thumb', callback_data='thumb')
).row(
    InlineKeyboardButton('Download', callback_data='download')
)

sec1_kb = InlineKeyboardMarkup().row(
    InlineKeyboardButton('Back', callback_data='back'),
)

sec2_kb = InlineKeyboardMarkup().row(
    InlineKeyboardButton('Delete', callback_data='delete'),
).row(
    InlineKeyboardButton('Back', callback_data='back'),
)
