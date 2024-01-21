import sqlite3
from aiogram import types

from data.config import ADMINS
from loader import dp, db
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters.builtin import Command


@dp.message_handler(text='/alltestbooks', user_id=ADMINS)
async def get_all_test_books(msg: types.Message):
    test_books = db.select_all_answers()
    t_b = 'Bazadagi barcha test kitoblar:\n'
    num = 1
    for test_book in test_books:
        t_b += f'{num}. {test_book[1]}\n'
        num += 1
    await msg.answer(t_b)


@dp.message_handler(Command('addtestbooknumber'), user_id=ADMINS)
async def answer_keys(msg: Message, state: FSMContext):
    await msg.answer("Test kitob raqami va unga bog'langan javoblarni kiriting.\nNamuna: 1234567:ABCDABCDABCD...")
    await state.set_state('addtestbooknumber')


@dp.message_handler(Command('deletedatabase'), user_id=ADMINS)
async def delete_db(msg: Message):
    db.delete_db()
    await msg.answer("Baza o'chirib yuborildi")


@dp.message_handler(state='addtestbooknumber')
async def add_test_book_number(msg: Message, state: FSMContext):
    answer_key = msg.text
    book_num = answer_key.split(':')[0]
    keys = answer_key.split(':')[-1]
    db_data = db.select_all_answers()
    book_numbers = []
    for num in db_data:
        book_numbers.append(num[1])
        print(book_numbers)
    try:
        if len(book_num) == 7 and len(keys) == 90:
            if int(book_num) not in book_numbers:
                db.add_answer(book_number=int(book_num), answers=keys)
                await msg.reply('Muvaffaqqiyatli saqlandi  ✅.')
                await state.finish()
            else:
                await msg.answer(f'Bu  {book_num}  test kitobi raqami bazada mavjud. Boshqa kiriting.  /addtestbooknumber')
                await state.finish()
        else:
            await msg.reply("Qandaydir xatolik sodir bo'ldi ❌. Test kitobi raqami yoki javoblarda kamchilik bor.\nIltimos qaytadan urinib ko'ring!  /addtestbooknumber")
            await state.finish()
    except sqlite3.IntegrityError as e:
        await msg.answer('No success...')
        await state.finish()
