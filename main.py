import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import ChatMember

API_TOKEN = ''
CHAT_ID = '-1001263394243'
CHANNEL_USERNAME = 'KvartirochkaOfficial'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# команда /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # получите id пользователя и id чата
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # проверьте, подписан ли пользователь на канал
    member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
    is_subscribed = member.status == 'member'
    
    if is_subscribed:
        await message.answer('Вы уже подписаны на наш канал. '
                             'Теперь вы можете оставлять свои сообщения в этом чате.')
    else:
        await message.answer('Добро пожаловать в чат! '
                             'Пожалуйста, подпишитесь на наш канал, чтобы продолжить общение: '
                             't.me/{}'.format(CHANNEL_USERNAME))
        # установите мьют для участника, чтобы запретить ему отправлять сообщения
        await bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)

# обработчик изменения статуса участника чата
@dp.message_handler(ChatMember(update_types=['chat_member']))
async def on_chat_member_update(message: types.Message):
    # проверьте, что пользователь изменил статус подписки на канал
    chat_id = message.chat.id
    user_id = message.from_user.id
    member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
    is_subscribed = member.status == 'member'
    
    # если пользователь только что подписался на канал, разрешите ему отправлять сообщения
    if is_subscribed:
        await bot.restrict_chat_member(chat_id, user_id, can_send_messages=True)
        await message.answer('Спасибо за подписку на наш канал! Теперь вы можете писать в этот чат.')

if __name__ == '__main__':
    logging.info('Starting bot...')
    dp.start_polling()
