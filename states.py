

from aiogram.dispatcher.filters.state import State, StatesGroup


class Incomes(StatesGroup):
    income = State()


class Expenses(StatesGroup):
    expenses = State()


class Savings(StatesGroup):
    savings = State()
