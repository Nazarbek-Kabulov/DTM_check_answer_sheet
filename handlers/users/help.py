from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "/imagesample - Namuna rasmlar",
            "/alltestbooks - Bazada mavjud test kitobi raqamlar",
            "/addtestbooknumber - Bazaga test javoblarini qo'shish")
    
    await message.answer("\n".join(text))
