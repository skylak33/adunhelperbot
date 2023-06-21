import time
import logging
import asyncio
import config
from base import *
from states import *

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
    keyboard.add("Доходы", "Расходы")
    keyboard.add("Сбережения", "Статистика")
    keyboard.add("Способы заработка")
    await message.answer(f"Привет, @{alias}, я @adunhelperbot, цифровой финансовый помощник для подростков. Моя цель помочь вам составить бюджет, указывая на ваши доходы и расходы. Это позволит вам лучше понять, как распределять свои деньги и контролировать свои финансы.", reply_markup=keyboard)
    db_add_user(user_id, f'@{alias}')

    current_savings = db_get_savings

    if current_savings is None:
        await Savings.savings.set()
    else:
        print("OK")


@dp.message_handler(state=Savings.savings)
async def input_expenses(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text.isdigit():
        db_update_savings(user_id, float(message.text))
        await state.finish()
        current_savings = db_get_savings(user_id)
        await message.answer(f"Ваши сбережния был успеешно изменены. На данный момент ваши расходы составляют: {current_savings}")
    else:
        await message.answer("Введите цифрами :")

# Доходы


@dp.message_handler(text="Доходы")
async def with_puree(message: types.Message):
    await message.answer("Введите ваши доходы :")
    await Incomes.income.set()


@dp.message_handler(state=Incomes.income)
async def input_incomes(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text.isdigit():
        db_update_income(user_id, float(message.text))
        await state.finish()
        current_income = db_get_income(user_id)
        db_update_savings(user_id, db_get_income(
            user_id), db_get_expenses(user_id))
        await message.answer(f"Ваш доход был успеешно добавлен. На данный момент ваш доход составляет: {current_income}")
    else:
        await message.answer("Введите цифрами:")
# _______________________________________________________________
# Расходы


@dp.message_handler(text="Расходы")
async def with_puree(message: types.Message):
    await message.answer("Введите ваши расходы :")
    await Expenses.expenses.set()


@dp.message_handler(state=Expenses.expenses)
async def input_expenses(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text.isdigit():
        db_update_expenses(user_id, float(message.text))
        await state.finish()
        current_expenses = db_get_expenses(user_id)
        db_update_savings(user_id, db_get_income(
            user_id), db_get_expenses(user_id))
        await message.answer(f"Ваши расходы был успеешно добавлены. На данный момент ваши расходы составляют: {current_expenses}")
    else:
        await message.answer("Введите цифрами :")
# _______________________________________________________________
# Сбережения


@dp.message_handler(text="Сбережения")
async def with_puree(message: types.Message):
    user_id = message.from_user.id
    current_savings = db_get_savings(user_id)

    await message.answer(f"Ваши сбережния на данный момент ваши составляют: {current_savings}")


@dp.message_handler(text="Способы заработка")
async def cmd_inline_url(message: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Онлайн", callback_data="Онлайн"),
        types.InlineKeyboardButton(text="Офлайн", callback_data="Офлайн")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Я могу предложить тебе 2 способа заработка. Первый  способ заработка. Биржа фриланса и онлайн игры — это место, где ты можешь заработать в интернете. Второй способ заработка. офлайн-работа для подростка - это простые работы (уборка, покраска, расклейка объявлений), на которые  можно устроиться без проблем.", reply_markup=keyboard)


@dp.callback_query_handler(text="Онлайн")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Если ты хорошо владеешь Photoshop или Premiere pro,то ты можешь найти много заказов на бирже фриланса. Если ты хорошо играешь в игры, то я могу предложить заработать на этом.\n"
                              "1. На сайте: https://funpay.com/ можешь выбрать игру, в которую ты хорошо играешь и увидишь, как, играя можно зарабатывать.\n"
                              "2. На сайте: https://www.fl.ru/ ты сможешь найти себе заказы по обработке фотографий или видео.\n"
                              "3. На сайте: https://www.anketka.ru/ru/  ты сможешь проходить опросы, благодаря чему будешь зарабатывать на этом деньги.\n")


@dp.callback_query_handler(text="Офлайн")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Заработок в реальной жизни. Это простая работа, где тебя могут взять без опыта работы и образования.\n"
                              "https://hh.ru/  на этом сайте ты сможешь найти подработку на свой вкус.")


if __name__ == "__main__":
    executor.start_polling(dp)
