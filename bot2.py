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
    await message.answer(f"Привет, @{alias}, я @adunhelperbot, цифровой финансовый помощник для подростков. Моя цель помочь вам составить бюджет, указывая на ваши доходы и расходы. Это позволит вам лучше понять, как распределять свои деньги и контролировать свои финансы.", reply_markup=keyboard)
    db_add_user(user_id, f'a{alias}')

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
        await message.answer("Ваш доход был успеешно добавлен. На данный момент ваш доход :")
    else:
        await message.answer("Введите цифрами, даун тупой, твою мать ебал :")

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
        await message.answer("Ваши расходы был успеешно добавлены. На данный момент ваши расходы :")
    else:
        await message.answer("Введите цифрами, даун тупой, твою мать ебал :")


@dp.message_handler(text="Сбережения")
async def with_puree(message: types.Message):
    await message.answer("Ваши сбережение :")

if __name__ == "__main__":
    executor.start_polling(dp)
