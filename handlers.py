from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart

import keyboards
import config
import database
import api_requests
import main

router = Router()

class Request_text(StatesGroup):
    text = State()



@router.message(CommandStart())
async def user_start(message:Message):
    if  message.from_user.id in config.ADMIN_LIST:
        await database.add_user(message.from_user.id)
        await message.answer('Привет, я бесплатный текстовый генератор Gemini\nИспользуй кнопки на клавиатуре, чтобы воспользоваться моим функционалом\nДля запроса просто отправь сообщение', reply_markup=keyboards.start_keyboard)
    else:
        await database.add_user(message.from_user.id)
        await message.answer('Привет, я бесплатный текстовый генератор Gemini\nИспользуй кнопки на клавиатуре, чтобы воспользоваться моим функционалом\nДля запроса просто отправь сообщение', reply_markup=keyboards.start_keyboard)

@router.message(F.text=='Мой профиль')
async def user_profile(message:Message):

    user_requests = await database.get_requests(message.from_user.id)
    await message.answer(f'Ваш профиль:\n\nИмя: {message.from_user.first_name}\n\nКоличество оставшихся запросов: {str(user_requests)}')

@router.message(F.text=='Информация')
async def information(message:Message):
    await message.answer('Данный бот разработан в развлекательных целях(но я пиздец заебался), вы можете делать текстовые запросы бла бла бла \nКонтакты: @recoil_sss')

@router.message(F.text)
async  def user_make_request(message:Message):
    await message.answer('Ожидайте ответа...')
    user_history = await database.user_history(message.from_user.id)
    request_answer = api_requests.text_request(message.text, user_history)

    if request_answer:
        await database.made_request(message.from_user.id, message.text)
        await message.answer(request_answer)

    else:
        await  message.answer('Не удалось осуществить запрос')
         
