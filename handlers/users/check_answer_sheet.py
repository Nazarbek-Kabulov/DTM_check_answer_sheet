import sqlite3
from aiogram import types
from aiogram.types import ContentType, Message
from loader import dp, db
from pathlib import Path

from .answer_sheet.functions.check_answer import check_answer
from .answer_sheet.functions.read_answer import answer_sheet

download_path = Path().joinpath('downloads')
download_path.mkdir(parents=True, exist_ok=True)


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def any_type(message: Message):
    # Download the document file
    document_path = await message.document.download(download_path)

    # Check if the file download was successful
    if document_path:
        # Call the answer_sheet function with the downloaded file's path
        await message.answer('Please a wait!')

        result = answer_sheet(document_path.name)
        data = check_answer(result)
        # Check the result and send a reply
        if result == 'No result':
            await message.reply(f'{result} 🤷‍♂️.\nBecause, image received incorrectly, please see "Sample images"!\nCommand  /imagesample')
        else:
            await message.reply(f'Natija:\n{data}')
    else:
        await message.reply('Failed to download the document. Please try again.')

    # Optionally, you can delete the downloaded file to free up storage space
    file_path = Path(document_path.name)
    file_path.unlink()

