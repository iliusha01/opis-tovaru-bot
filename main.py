from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import logging

API_TOKEN = '7593968750:AAEqxf9xqvZPOzLpzwW3FFVfUVu804OSzBg'
ADMIN_ID = 920291804
CHANNEL_LINK = 'https://t.me/+N2JJml7IIOthNzE6'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_data[message.from_user.id] = {}
    await message.answer("Привіт! Напиши, будь ласка, своє ім'я:")

@dp.message_handler(lambda message: message.from_user.id in user_data and 'name' not in user_data[message.from_user.id])
async def name_handler(message: types.Message):
    user_data[message.from_user.id]['name'] = message.text
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("📞 Надати номер телефону", request_contact=True)
    keyboard.add(button)
    await message.answer("Чудово! Тепер натисни кнопку нижче, щоб поділитись своїм номером телефону:", reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact_handler(message: types.Message):
    user = message.from_user
    contact = message.contact.phone_number
    name = user_data.get(user.id, {}).get('name', 'Невідомо')
    username = user.username or 'Немає'

    # Повідомлення адміну
    admin_message = (
        f"🆕 Новий контакт\n"
        f"👤 Ім'я: {name}\n"
        f"📞 Телефон: {contact}\n"
        f"🔗 Username: @{username}"
    )
    await bot.send_message(ADMIN_ID, admin_message)

    # Повідомлення користувачу
    await message.answer("✅ Дякуємо за надану інформацію!\n\nОсь посилання на наш канал з товарами та повними описами:", reply_markup=ReplyKeyboardRemove())
    await message.answer(CHANNEL_LINK)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
