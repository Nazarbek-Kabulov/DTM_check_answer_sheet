from loader import db


def check_answer(result):
    if result != 'No result':
        find_book_num = result.split(':')[0]
        find_answers = result.split(':')[1]
        db_data = db.select_all_answers()
        book_nums = []
        for i in db_data:
            book_nums.append(i[1])

        answer_relust = []
        answer_relust_ = ''
        right_answer = 0
        wrong_answer = 0
        maj_fan = 0
        fan_4 = 0
        fan_5 = 0

        if int(find_book_num) in book_nums:
            for i in db_data:
                if int(find_book_num) == i[1]:
                    for k in range(len(i[2])):
                        if find_answers[k] == i[2][k]:
                            answer_relust.append(f'{k+1}. {find_answers[k]}   ✅')
                            right_answer += 1
                        else:
                            answer_relust.append(f'{k+1}. {find_answers[k]}   ❌')
                            wrong_answer += 1
            for i in answer_relust[:30]:
                if i[-1] == '✅':
                    maj_fan += 1
            for i in answer_relust[30:60]:
                if i[-1] == '✅':
                    fan_4 += 1
            for i in answer_relust[60:]:
                if i[-1] == '✅':
                    fan_5 += 1
            for i in answer_relust:
                answer_relust_ += i
                answer_relust_ += '\n'
            ball = maj_fan * 1.1 + fan_4 * 2.1 + fan_5 * 3.1
            data = f"{answer_relust_}\n\nTo'g'ri javoblar soni:  {right_answer}\nNoto'g'ri javoblar soni:  {wrong_answer}\nBall:  {round(ball, 1)}"
            return data
        else:
            return f'Bu  {find_book_num}  test kitobi bazada mavjud emas!!!'
    else:
        return result
