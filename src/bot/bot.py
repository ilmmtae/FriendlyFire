import asyncio
import logging

import httpx

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from src.api.redis import get_user_id_by_token
from src.config.config import settings
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message



logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
storage = RedisStorage(redis)
dp = Dispatcher(storage=storage)
http_client = httpx.AsyncClient(base_url="http://127.0.0.1:8000")


class MyStates(StatesGroup):
    waiting_for_phone = State()


@dp.shutdown()
async def shutdown_bot(dispatcher: Dispatcher):
    await http_client.aclose()

@dp.message(Command("start"))
async def cmd_start(message: Message, command: CommandObject, state: FSMContext):
    short_token = command.args

    if not short_token:
        await message.answer("Please use the generated link.")
        return

    await state.update_data(token=short_token)
    await state.set_state(MyStates.waiting_for_phone)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Share contact", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer("Authentication successful!", reply_markup=kb)


@dp.message(MyStates.waiting_for_phone, F.contact)
async def handle_contact(message: types.Message, state: FSMContext):
    data = await state.get_data()
    token = data.get("token")
    logging.info(f"Sending token to API: {token}")
    phone = message.contact.phone_number

    response = await http_client.post(
        "/authentication/verify-deeplink",
        json={"token": token, "phone": phone}
    )

    if response.status_code == 200:
        await message.answer("Success!")
    else:
        await message.answer("Verification failed.")
    await state.clear()


@dp.message()
async def handle_everything(message: Message, state: FSMContext):
    if not message.text.startswith('/start'):
        if "." in message.text and len(message.text) > 50:
             pass



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

