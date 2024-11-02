from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, 
                           InlineKeyboardButton, InlineKeyboardMarkup)

start_keyboard = ReplyKeyboardMarkup(keyboard=[
     [KeyboardButton(text='Мой профиль'),
     KeyboardButton(text='Информация')]
], resize_keyboard=True)

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
     [KeyboardButton(text='Мой профиль'),
     KeyboardButton(text='Информация')],
     [KeyboardButton(text='Запустить рассылку')]
], resize_keyboard=True)