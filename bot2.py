import time
import logging
import asyncio
import config
from base import *
from states import *
from random import *
import statistic
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputFile
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
    keyboard.add("Доходы", "Расходы", "Сбережения")
    keyboard.add("Советы", "Способы заработка")
    keyboard.add("Проверка финансовой грамотности")
    await message.answer(
        f"[👋] Приветствую тебя, @{alias} \n"
        f"[🌺] С тобой на связь вышел - @adunhelperbot: \n"
        f"Цифровой финансовый помощник для подростков. \n"
        f"\n"
        f"                      ══════ஜ▲ஜ══════ \n"
        f"[💡] Моя цель - это помочь Вам составить бюджет, \n"
        f"указывая на ваши доходы и расходы. \n"
        f"                      ══════ஜ▲ஜ══════ \n"
        f"\n"
        f"[☀️] Это позволит вам лучше понять, как распределять \n"
        f"свои деньги и контролировать свои финансы. \n",
        reply_markup=keyboard
    )
    db_add_user(user_id, f'@{alias}')
    current_savings = db_get_savings(user_id)

@dp.message_handler(state=Savings.savings)
async def init_expenses(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer("Введите ваши первоначальные сбережения :")
    if message.text.isdigit():
        db_init_savings(user_id, float(message.text))
        await state.finish()
        current_savings = db_get_savings(user_id)
        await message.answer(f"Ваши сбережния был успеешно изменены. На данный момент ваши расходы составляют: {current_savings}")
    else:
        await message.answer("Введите цифрами :")


@dp.message_handler(text="Проверка финансовой грамотности" or "Да")
async def start_handler_1(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="220", callback_data="Да"),
        types.InlineKeyboardButton(text="22", callback_data="Нет"),
        types.InlineKeyboardButton(text="228", callback_data="Нет"),
        types.InlineKeyboardButton(text="2200", callback_data="Нет"),
        types.InlineKeyboardButton(text="Еще вопрос", callback_data="Еще1")

    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer("В банк был положен вклад под 10% годовых. Через год, после начисления процентов, вкладчик снял со счета 2000 рублей, а еще через год (опять после начисления процентов) снова внес 2000 рублей. Вследствие этих действий через три года со времени открытия вклада вкладчик получил сумму меньше запланированной (если бы не было промежуточных операций со вкладом). На сколько рублей меньше запланированной суммы он получил?", reply_markup=keyboard)


@dp.callback_query_handler(text="Да")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Верно. За 3 года хранения этих денег вклад вырос бы в 1.331 раз")


@dp.callback_query_handler(text="Нет")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Неверно. За 3 года хранения этих денег вклад вырос бы в 1.331 раз. Запланированный и фактический проценты за первый год не отличаются. Тогда ответ равен 220")
    return
@dp.callback_query_handler(text="Да1")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Верно.")


@dp.callback_query_handler(text="Нет1")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Неверно. ")
    return

@dp.callback_query_handler(text="Еще1")
async def send_random_value(call: types.CallbackQuery):
    lenv = statistic.lenv
    number = randint(0, lenv - 1)
    quest = statistic.v[number]
    answers = statistic.v0[number]
    buttons = [
        types.InlineKeyboardButton(text=answers[2], callback_data="Да1"),
        types.InlineKeyboardButton(text=answers[1], callback_data="Нет1"),
        types.InlineKeyboardButton(text=answers[0], callback_data="Нет1"),
        types.InlineKeyboardButton(text="Еще вопрос", callback_data="Еще1")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.message.answer(quest, reply_markup=keyboard)

# Доходы


@dp.message_handler(text="Доходы")
async def with_puree(message: types.Message):
    await message.answer("Введите ваши доходы :")
    await Incomes.income.set()


@dp.message_handler(state=Incomes.income)
async def input_incomes(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    datatime = time.time()
    date = time.ctime(datatime)
    if message.text.isdigit():
        db_update_income(user_id, float(message.text), datatime, date, 1)
        await state.finish()
        current_income = db_get_income(user_id)
        db_update_savings(user_id)
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
    datatime = time.time()
    date = time.ctime(datatime)
    if message.text.isdigit():
        db_update_expenses(user_id, float(message.text), datatime, date, 0)
        await state.finish()
        current_expenses = db_get_expenses(user_id)
        db_update_savings(user_id)
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
    await call.message.answer("Сайт https://www.fl.ru/, здесь ты сможешь найти себе заказы по обработке фотографий или монтажу видео.\nСайт https://funpay.com/, здесь ты сможешь зарабатывать деньги, просто играя в игры.\nТакже есть сайт https://www.anketka.ru/ru/, где ты сможешь зарабатывать деньги, просто проходя опросы.")


@dp.callback_query_handler(text="Офлайн")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Заработок в реальной жизни.\nНа сайте  https://hh.ru/  ты сможешь найти свою первую работу, стажировку или подработку. Размещай своё резюме и просматривай интересные вакансии от работодателей. ")


@dp.message_handler(text="Советы")
async def cmd_inline_url_1(message: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Eще", callback_data="Еще"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await message.answer(f"Совет, который пригодится в взрослой жизни :\n \n{statistic.s[randint(0, statistic.lens - 1)]}", reply_markup=keyboard)


@dp.callback_query_handler(text="Еще")
async def send_random_value(call: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Eще", callback_data="Еще"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.answer(statistic.s[randint(0, statistic.lens - 1)], reply_markup=keyboard)


@dp.message_handler(text="Дота")
async def cmd_inline_url_1(message: types.CallbackQuery):
    photo = InputFile("pudge.jpeg")

    await bot.send_photo(chat_id=message.chat.id, photo=photo)
if __name__ == "__main__":
    executor.start_polling(dp)
