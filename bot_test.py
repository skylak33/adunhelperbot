import time
import logging
import asyncio
import config
from base import *
from states import *
import statistic
from random import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

MSG = "Программировал ли ты сегодня, {}?"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.token)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    alias = message.from_user.username
    logging.info(f'{user_id} {alias} {time.asctime()}')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Проверка финансовой грамотности")
    keyboard.add("Советы", "Статистика")
    keyboard.add("Способы заработка")
    await message.answer(f"Привет, @{alias}, я @adunhelperbot, цифровой финансовый помощник для подростков. Моя цель помочь вам составить бюджет, указывая на ваши доходы и расходы. Это позволит вам лучше понять, как распределять свои деньги и контролировать свои финансы.", reply_markup=keyboard)


@dp.message_handler(text="Способы заработка")
async def cmd_inline_url(message: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Онлайн", callback_data="Онлайн"),
        types.InlineKeyboardButton(text="Офлайн", callback_data="Офлайн")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Я могу предложить тебе 2 способа заработка. Первый  способ заработка. Биржа фриланса и онлайн игры — это место, где ты можешь заработать в интернете. Второй способ заработка. офлайн-работа для подростка - это простые работы (уборка, покраска, расклейка объявлений), на которые  можно устроиться без проблем.", reply_markup=keyboard)


@dp.message_handler(text="Советы")
async def cmd_inline_url_1(message: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Eще", callback_data="Еще"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer(statistic.s[randint(0, statistic.lens - 1)], reply_markup=keyboard)


@dp.callback_query_handler(text="Онлайн")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Если ты хорошо владеешь Photoshop или Premiere pro,то ты можешь найти много заказов на бирже фриланса. Если ты хорошо играешь в игры, то я могу предложить заработать на этом."
                              "на сайте: https://funpay.com/ можешь выбрать игру, в которую ты хорошо играешь и увидишь, как, играя можно зарабатывать."
                              "на сайте: https://www.fl.ru/ ты сможешь найти себе заказы по обработке фотографий или видео."
                              "на сайте: https://www.anketka.ru/ru/  ты сможешь проходить опросы, благодаря чему будешь зарабатывать на этом деньги.")
    cmd_inline_url()


@dp.callback_query_handler(text="Офлайн")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Заработок в реальной жизни. Это простая работа, где тебя могут взять без опыта работы и образования. https://hh.ru/  на этом сайте ты сможешь найти подработку на свой вкус.")

    cmd_inline_url()


@dp.callback_query_handler(text="Еще")
async def send_random_value(call: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Eще", callback_data="Еще"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.answer(statistic.s[randint(0, statistic.lens - 1)], reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp)
