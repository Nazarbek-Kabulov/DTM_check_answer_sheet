import types

from loader import dp
from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters.builtin import Command


@dp.message_handler(Command('imagesample'))
async def imagesample(msg: Message):
    await msg.answer_photo('AgACAgIAAxkBAAICy2Wr81Df_H-mhSrNgz21pYnUVUTHAALG1TEbf3BZSVlQHwvITWsOAQADAgADeQADNAQ')


@dp.message_handler(content_types=ContentType.PHOTO)
async def send_photo(msg: Message):
    await msg.reply(msg.photo[-1].file_id)
