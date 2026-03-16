import asyncio
import random

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from database import add_word, get_words

TOKEN = "8644335191:AAEemv8QE--QT3SZpcJGH4yQ4hyWj4_4J7Y"

bot = Bot(token=TOKEN)
dp = Dispatcher()

current_words = {}


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Salom!\n\n"
        "Bu lug'at yodlash bot.\n\n"
        "So'z qo'shish:\n"
        "/addword Apple - Olma\n\n"
        "Mashq qilish:\n"
        "/learn"
    )


@dp.message(Command("addword"))
async def add_word_command(message: Message):

    try:

        text = message.text.replace("/addword", "").strip()

        word, translation = text.split("-")

        word = word.strip()
        translation = translation.strip()

        result = add_word(message.from_user.id, word, translation)

        if result:
            await message.answer(
                f"So'z saqlandi ✅\n\n"
                f"{word.capitalize()} — {translation.capitalize()}"
            )

        else:
            await message.answer(
                "Bu so'z allaqachon lug'atingizda bor ⚠️"
            )

    except:

        await message.answer(
            "To'g'ri format:\n\n"
            "/addword Apple - Olma"
        )


@dp.message(Command("learn"))
async def learn(message: Message):

    words = get_words(message.from_user.id)

    if not words:
        await message.answer("Avval so'z qo'shing ⚠️")
        return

    word, translation = random.choice(words)

    current_words[message.from_user.id] = word

    await message.answer(f"{translation}\n\nInglizchasini yozing")


@dp.message()
async def check_answer(message: Message):

    user_id = message.from_user.id

    if user_id not in current_words:
        return

    correct_word = current_words[user_id]

    if message.text.lower() == correct_word.lower():

        await message.answer("✅ To'g'ri")

    else:

        await message.answer(
            f"❌ Xato\n\nTo'g'ri javob: {correct_word}"
        )

    words = get_words(user_id)

    word, translation = random.choice(words)

    current_words[user_id] = word

    await message.answer(
        f"{translation}\n\nInglizchasini yozing"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())