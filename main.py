import asyncio
import json
import logging

import aiohttp
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart


from settings import BOT_TOKEN, API_KEY

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher()

async def get_current_weather(city:str) -> str:
    async with aiohttp.ClientSession() as session:
        response = await session.get(f'https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=RU')
        result = await response.json()
        if response.status == 200:
            message = (f'В городе {result['location']['name']} температура воздуха равняется {round(result['current']['temp_c'])}° по Цельсию. '
                       f'{result['current']['condition']['text']}, влажность: {result['current']['humidity']}%, '
                       f'скорость ветра {result['current']['wind_kph']} км в час.')
        else:
            if result['error']['code'] == 1006:
                message = "Я не смог найти нужный город!"
            if result['error']['code'] == 9999:
                message = 'Внутренняя ошибка сервера! Повторите ваш запрос позже!'
        return message

@dispatcher.message(CommandStart())
async def on_start(message: types.Message):
    await message.answer(text="Добрый день! Давайте узнаем погоду в интересующем Вас городе, введите его название.")


@dispatcher.message()
async def echo_message(message: types.Message):
    if message.text:
        weather = await get_current_weather(message.text)
        await message.answer(text=weather)
    else:
        await message.answer(text="Пожалуйста, введите корректное название города!")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())