from aiogram import Bot, Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import random
import asyncio

# Инициализация бота
API_TOKEN = '7730531387:AAGzqq6YXjJ_rbqdWKp7T_A1yqAOIUwFD8g'  # Замени на токен от @BotFather
bot = Bot(token=API_TOKEN)
router = Router()

# Список букв русского алфавита
LETTERS = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

# Определяем состояния для игры
class GameStates(StatesGroup):
    WAITING_FOR_WORDS = State()

# Храним данные игры
game_data = {
    'current_letter': None,
    'scores': {},
    'current_player': None
}

# Команда /start
@router.message(Command('start'))
async def start_game(message: types.Message):
    await message.reply("Привет! Это игра с буквами. Напиши /newgame, чтобы начать новую игру!")

# Команда /newgame
@router.message(Command('newgame'))
async def new_game(message: types.Message, state: FSMContext):
    await message.reply("Новая игра началась! Первый игрок, готовьтесь...")
    letter = random.choice(LETTERS)
    game_data['current_letter'] = letter
    game_data['current_player'] = message.from_user.id
    await message.reply(f"Буква: {letter}. У вас 90 секунд, называйте слова!")
    await state.set_state(GameStates.WAITING_FOR_WORDS)
    
    # Таймер
    await asyncio.sleep(90)
    await message.reply("Время вышло!")
    await state.clear()

# Обработчик слов
@router.message(GameStates.WAITING_FOR_WORDS)
async def process_word(message: types.Message, state: FSMContext):
    word = message.text.lower().strip()
    if word.startswith(game_data['current_letter'].lower()):
        user_id = message.from_user.id
        game_data['scores'][user_id] = game_data['scores'].get(user_id, 0) + 1
        await message.reply(f"Слово '{word}' принято! +1 очко")
    else:
        await message.reply(f"Слово должно начинаться на '{game_data['current_letter']}'!")

# Запуск бота
async def main():
    from aiogram import Dispatcher
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())