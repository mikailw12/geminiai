import asyncio
from aiogram import Dispatcher, Bot
from config import TOKEN, ADMIN_LIST
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from api_requests import text_request
from database import user_history, get_requests, made_request, get_users, add_user, Base, engine
from keyboards_bot import start_keyboard, admin_keyboard

bot = Bot(token=TOKEN)
dp = Dispatcher()

class spam_text(StatesGroup):
    text = State()



@dp.message(CommandStart())
async def user_start(message:Message):
    if  message.from_user.id in ADMIN_LIST:
        await add_user(message.from_user.id)
        await message.answer('Привет, я бесплатный текстовый генератор Gemini\nИспользуй кнопки на клавиатуре, чтобы воспользоваться моим функционалом\nДля запроса просто отправь сообщение', reply_markup=admin_keyboard)
    else:
        await add_user(message.from_user.id)
        await message.answer('Привет, я бесплатный текстовый генератор Gemini\nИспользуй кнопки на клавиатуре, чтобы воспользоваться моим функционалом\nДля запроса просто отправь сообщение', reply_markup=start_keyboard)

@dp.message(F.text=='Мой профиль')
async def user_profile(message:Message):

    user_requests = await get_requests(message.from_user.id)
    await message.answer(f'Ваш профиль:\n\nИмя: {message.from_user.first_name}\n\nКоличество оставшихся запросов: {str(user_requests)}')

@dp.message(F.text=='Информация')
async def information(message:Message):
    await message.answer('Данный бот разработан в развлекательных целях(но я пиздец заебался), вы можете делать текстовые запросы бла бла бла \nКонтакты: @recoil_sss')

         
@dp.message(F.text=='Текстовая рассылка')
async def spam(message:Message, state:FSMContext):
    if message.from_user.id in ADMIN_LIST:
        await message.answer('Введите текст для рассылки,\nГлавное меню - /start')
        await state.set_state(spam_text.text)


@dp.message(spam_text.text)
async def start_spam(message: Message, state: FSMContext):
    # Сохранение текста, который ввел пользователь (администратор)
    await state.update_data(text=message.text)
    
    data = await state.get_data()  # Получаем данные состояния
    await state.clear()  # Сбрасываем состояние после получения данных
    
    admin_text = data.get("text")
    users_id = await get_users()  # Получение списка пользователей
    for user_id in users_id:
        await bot.send_message(chat_id=user_id, text=f'{admin_text}')


@dp.message(F.text)
async  def user_make_request(message:Message):
    wait_message = await message.answer('Ожидайте ответа...')
    user_history = await user_history(message.from_user.id)
    request_answer = text_request(message.text, user_history)

    if request_answer:
        await made_request(message.from_user.id, message.text)
        await message.answer(request_answer)
        await bot.delete_message(chat_id=message.from_user.id, message_id=wait_message.message_id)
    else:
        await  message.answer('Не удалось осуществить запрос')








async def main():
    Base.metadata.create_all(engine)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')





