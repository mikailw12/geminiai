from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart

import keyboards
from config import bot, ADMIN_LIST
import database
import api_requests

router = Router()

class spam_text(StatesGroup):
    text = State()



@router.message(CommandStart())
async def user_start(message:Message):
    if  message.from_user.id in ADMIN_LIST:
        await database.add_user(message.from_user.id)
        await message.answer('Привет, я бесплатный текстовый генератор Gemini\nИспользуй кнопки на клавиатуре, чтобы воспользоваться моим функционалом\nДля запроса просто отправь сообщение', reply_markup=keyboards.admin_keyboard)
    else:
        await database.add_user(message.from_user.id)
        await message.answer('Привет, я бесплатный текстовый генератор Gemini\nИспользуй кнопки на клавиатуре, чтобы воспользоваться моим функционалом\nДля запроса просто отправь сообщение', reply_markup=keyboards.start_keyboard)

@router.message(F.text=='Мой профиль')
async def user_profile(message:Message):
    user_requests = await database.get_requests(message.from_user.id)
    await message.answer(f'Ваш профиль:\n\nИмя: {message.from_user.first_name}\n\nКоличество оставшихся запросов: {str(user_requests)}\nГлавное меню - /start')

@router.message(F.text=='Информация')
async def information(message:Message):
    await message.answer('Данный бот разработан в развлекательных целях, вы можете делать текстовые запросы \nКонтакты: @recoil_sss\nГлавное меню - /start')


@router.message(F.text=='Текстовая рассылка')
async def spam(message:Message, state:FSMContext):
    if message.from_user.id in ADMIN_LIST:
        await message.answer('Введите текст для рассылки,\nГлавное меню - /start')
        await state.set_state(spam_text.text)


@router.message(spam_text.text)
async def start_spam(message:Message, state:FSMContext):
    from main import bot
    data = await state.get_data()
    await state.clear()
    admin_text = data.get("text")
    users_id = await database.get_users()
    for user_id in users_id:
        await bot.send_message(chat_id=user_id, text=f'{admin_text}')


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
         
