from site import removeduppaths
import sqlite3
from turtle import left, right
import telebot
from telebot import types
import time
import datetime
from Task import Task
from TimeTable import TimeTable

bot = telebot.TeleBot("5796025327:AAGmNucofDgGzNLKwvdoOndVaufaIxX3vvY")

count_button = 0
chill_durat = 0
list_tasks = [] # задачи на день
flag = False # флаг, показывающий назвал ли пользователь свои задачи
string_name_tasks = ""
is_time = False
list_name_tasks = []
count = 0 # count для того чтобы один раз вводить время
time_flag = False

time_table = TimeTable()


tomorrow = datetime.date.today() + datetime.timedelta(days=1)
tomorrow = tomorrow.strftime("%d-%m-%Y ")
print(tomorrow)


# защита от лохов
@bot.message_handler(content_types=['audio', 'document', 'sticker', 'video', 'voice', 'contact', 'first_name', 'last_name'
                                    'id', 'username', 'forward_from', 'video_note', 'game', 'photo', 'dice', 'poll', 'location'
                                    'venue', 'forward_from_chat', 'forward_from_message_id', 'forward_signature', 'forward_date'
                                    'is_automatic_forward', 'reply_to_message', 'animation'])
def fefefe(message):
    bot.send_message(message.from_user.id, 'не надо дядя')


def count_time(present_time, i): #неприятная возня со временем(сделал функцию чтобы не засорять main функцию)
    a = present_time.split(":")
    a[1], a[0] = int(a[1]), int(a[0])
    a[1] += int(i)
    a[0] += a[1] // 60
    if int(a[1]) % 60 < 10:
        a[1] = "0" + str(int(a[1]) % 60)
    if int(a[1]) > 60:
        a[1] -= 60 * (a[1] // 60)
    if int(a[1]) == 60:
        a[1] = "00"
    if int(a[1]) % 60 < 10:
        a[1] = "0" + str(int(a[1]) % 60)
    present_time = str(a[0]) + ":" + str(a[1])
    return present_time


def res_algorithm(message):

    left_tasks = []

    for i in time_table.list_tasks:
        left_tasks.append(i)
    present_time = time_table.start_time
    tomato = 25
    count = 0
    i = 0
    while i != len(left_tasks):

        if tomato <= 0:
            if count != 3:
                #bot.send_message(message.from_user.id, str(present_time) + " - отдых")

                conn = sqlite3.connect('base.db')
                cur = conn.cursor()
                # format datetime: YYYY-MM-DD HH:MI
                cur.execute("insert into scheduler (date, action, telegram_user_id) values (?, ?, ?);", (f'{tomorrow}' + str(present_time), ' - отдых', f'{int(str(message.from_user.id)[-5:])}'))
                conn.commit()

                tomato = 25
                present_time = count_time(present_time, 5)
                count += 1
            else:
                #bot.send_message(message.from_user.id, str(present_time) + " - отдых")

                conn = sqlite3.connect('base.db')
                cur = conn.cursor()
                # format datetime: YYYY-MM-DD HH:MI
                cur.execute("insert into scheduler (date, action, telegram_user_id) values (?, ?, ?);", (f'{tomorrow}' + str(present_time), ' - отдых', f'{int(str(message.from_user.id)[-5:])}'))
                conn.commit()

                tomato = 25
                present_time = count_time(present_time, 25)
                count = 0
        else:

            if int(left_tasks[i].duration) < tomato:
                tomato -= int(left_tasks[i].duration)
                #bot.send_message(message.from_user.id, str(present_time) + " - " + left_tasks[i].name_of_task)

                conn = sqlite3.connect('base.db')
                cur = conn.cursor()
                # format datetime: YYYY-MM-DD HH:MI
                cur.execute("insert into scheduler (date, action, telegram_user_id) values (?, ?, ?);", (f'{tomorrow}' + str(present_time), f'{left_tasks[i].name_of_task}', f'{int(str(message.from_user.id)[-5:])}'))
                conn.commit()

                present_time = count_time(present_time, int(left_tasks[i].duration))
                i += 1

            elif int(left_tasks[i].duration) >= tomato:
                #bot.send_message(message.from_user.id, str(present_time) + " - " + left_tasks[i].name_of_task)

                conn = sqlite3.connect('base.db')
                cur = conn.cursor()
                # format datetime: YYYY-MM-DD HH:MI
                cur.execute("insert into scheduler (date, action, telegram_user_id) values (?, ?, ?);", (f'{tomorrow}' + str(present_time), f'{left_tasks[i].name_of_task}', f'{int(str(message.from_user.id)[-5:])}'))
                conn.commit()

                present_time = count_time(present_time, abs(tomato))
                left_tasks[i].duration = int(left_tasks[i].duration) - abs(tomato)
                tomato = 0
                if int(left_tasks[i].duration) == 0:
                    i += 1
    bot.send_message(message.from_user.id, "Расписание составлено")
    timetable(message)



def algorithm(message):
    sum_durat = 0
    for i in time_table.list_tasks:
        sum_durat += int(i.duration)
    print(sum_durat)
    count_of_pom = sum_durat // 25
    res_chill = count_of_pom // 3 * 30 + 5 * (count_of_pom - count_of_pom // 3) + (sum_durat % 25)
    print(res_chill)
    print(int(time_table.finish_time.split(":")[0]) * 60 + int(time_table.finish_time.split(":")[1]) - (int(time_table.start_time.split(":")[0]) * 60 + int(time_table.start_time.split(":")[1])))
    if sum_durat + res_chill > int(time_table.finish_time.split(":")[0]) * 60 + int(time_table.finish_time.split(":")[1]) - (int(time_table.start_time.split(":")[0]) * 60 + int(time_table.start_time.split(":")[1])):
        bot.send_message(message.from_user.id, "Что-то ты переборщил, братанчик, время, уделенное на работу время меньше времени, которое будет потрачено на ворк")
    else:
        time_table.list_tasks = sorted(time_table.list_tasks, key=lambda x: (int(x.importance) , int(x.urgency)))
        time_table.list_tasks.reverse()
        string_name_tasks = ""
        for i in time_table.list_tasks:
            string_name_tasks = string_name_tasks + " " + str(i.name_of_task)
        string_name_tasks = string_name_tasks[1:]
        #bot.send_message(message.from_user.id, "отсортированные задачи: " + string_name_tasks)
        res_algorithm(message)


def timetable(message):
    con = sqlite3.connect('base.db')
    cur = con.cursor()
    result = ''
    a = cur.execute(f'''SELECT date FROM scheduler WHERE telegram_user_id = "{int(str(message.from_user.id)[-5:])}"''').fetchall()
    b = cur.execute(f'''SELECT action FROM scheduler WHERE telegram_user_id = "{int(str(message.from_user.id)[-5:])}"''').fetchall()
    for i in range(len(a)):
        bot.send_message(message.from_user.id, a[i][0] + ' ' + b[i][0])


def buttons_func(message):
    global string_name_tasks
    global time_table
    global list_tasks
    # обработка кнопок
    if message.text == "Вывести мои задачи":
        if len(string_name_tasks.split()) == 0:
            bot.send_message(message.from_user.id, "У вас нет задач")
        else:
            bot.send_message(message.from_user.id, "задачи: " + string_name_tasks)
    # elif message.text == "Изменить список задач":
    #     bot.send_message(message.from_user.id, "функция находится в разработке")
    # elif message.text == "Очистить список задач":
    #     time_table.list_tasks = []
    #     string_name_tasks = ""
    #     bot.send_message(message.from_user.id, "готово")
    #     bot.send_message(message.from_user.id, "на данный момент у вас нет задач")
    else: # только если всего 4 кнопки иначе elif. получается else выполняется при нажатии кнопки "составить расписание"
        #bot.send_message(message.from_user.id, "функция находится в разработке")
        if len(string_name_tasks.split()) == 0:
            bot.send_message(message.from_user.id, "лол сортировать то нечего :)")
        else:
            algorithm(message)


# начальная фразочка
@bot.message_handler(commands=['start'])
def start(message):
    global list_tasks
    global count
    global chill_durat
    global count_button
    global string_name_tasks
    global is_time
    string_name_tasks = ""
    list_tasks = []
    time_table.list_tasks = []
    chill_durat = 0
    if message.text == '/start':
        is_time = False
        count = 0
        count_button = 0

        #очистка бд
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        cur.execute(f"""DELETE from scheduler WHERE telegram_user_id >= {int(str(message.from_user.id)[-5:])}""").fetchall()
        con.commit()

        bot.send_message(message.from_user.id, "Привет, я бот, который поможет тебе сделать твой день продуктивным")
        # клавиатура
        keyboard = types.InlineKeyboardMarkup()
        # кнопка «Да»
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        # добавление кнопки в клавиатуру
        keyboard.add(key_yes)
        # кнопка «Нет»
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        # question = 'Ответите на несколько вопросов?'
        question = "Ты готов начать?"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    elif message.text == "Вывести мои задачи" or message.text == "Изменить список задач" or message.text == "Очистить список задач":
        buttons_func(message)
    # создание кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("Вывести мои задачи")
    btn2 = types.KeyboardButton("Изменить список задач")
    btn3 = types.KeyboardButton("Очистить список задач")
    btn4 = types.KeyboardButton("Составить расписание")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text="Теперь можно использовать кнопки".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, time_function)


# обработка выбора пользователя
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global flag
    global count_button
    # call.data это callback_data, которую мы указали при объявлении кнопки
    if call.data == "yes" and count_button == 0:

        count_button += 1
        bot.send_message(call.message.chat.id, 'Введите время начала и конца рабочего дня'
                                               'пример: 9:00; 20:00')
        flag = True

    if call.data == "no" and count_button == 0:
        count_button += 1
        bot.send_message(call.message.chat.id, text='Тогда до скорой встречи',
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')


def tasks_function(message):
    global list_tasks
    global time_table
    global string_name_tasks
    global list_name_tasks
    global is_time
    if message.text == "Вывести мои задачи" or message.text == "Изменить список задач" or message.text == "Очистить список задач" or message.text == "Составить расписание":
        buttons_func(message)
    elif message.text == "/start":
        start(message)
    else:
        list_tasks = []
        if len(message.text.split("; ")) > 0:
            # тупая проверка присутствует ли больше 1 задачи + что это не кнопка
            message_new = message.text.split("; ")
            for i in message_new:
                sp = i.split(" ") # начинаем разбираться где название задачи/важность/срочность/длительность
                name_of_task = sp[0]
                importance = sp[1]
                urgency = sp[2]
                duration = sp[3]
                if int(importance) > 10 or int(urgency) > 10:
                    bot.send_message(message.from_user.id, "неправильный формат отправки данных")
                else:
                    task = Task(name_of_task, importance, urgency, duration)
                    list_tasks.append(task)
            time_table.list_tasks = list_tasks

        else:
            sp = message.text.split(" ")
            name_of_task = sp[0]
            importance = sp[1]
            urgency = sp[2]
            duration = sp[3]
            if int(importance) > 10 or int(urgency) > 10:
                bot.send_message(message.from_user.id, "неправильный формат отправки данных")
            else:
                task = Task(name_of_task, importance, urgency, duration)
                list_tasks.append(task)
            time_table.list_tasks = list_tasks

        # код ниже - вывод задач, которые ввел пользователь

        for i in list_tasks:
            list_name_tasks.append(i.name_of_task)
        string_name_tasks = ""
        for i in list_name_tasks:
            string_name_tasks = string_name_tasks + " " + str(i)
        string_name_tasks = string_name_tasks[1:]
        bot.send_message(message.from_user.id, 'отлично! нажмите на кнопку "составить расписание"')


@bot.message_handler(content_types=['text'])
def time_function(message):
    global count
    global flag
    if message.text == "Вывести мои задачи" or message.text == "Измнеить список задач" or message.text == "Очистить список задач" or message.text == "Составить расписание":
        buttons_func(message)
    elif count >= 1:
        tasks_function(message)

    elif message.text == "/start":
        start(message)

    else:
        semicolon = 0
        colon = 0
        for elem in message.text:
            if elem == ';':
                semicolon += 1
            if elem == ':':
                colon += 1
        if (semicolon == 1) and (colon == 2) and count == 0 and flag == True:
            semicolon = 0
            colon = 0

            global is_time
            global count_button
            global list_tasks
            global time_table
            global start_time
            global finish_time

            try:
                for i in message.text.split('; '):
                    time.strptime(i, '%H:%M')
                    count_button += 1
                    sp = message.text.split(";") # разбираемся где начальное и конечное время
                    start_time = sp[0]
                    finish_time = sp[1]
                time_table = TimeTable(start_time, finish_time, list_tasks)
                is_time = True
                print(time_table.start_time, time_table.finish_time, time_table.list_tasks)
                bot.send_message(message.from_user.id, 'введите список задач в формате: название задачи срочность(от 1 до 10) (важность(от 1 до 10) продолжительность(в минутах) пример: поесть 10 8 15; ауджимания 10 10 90')
                count += 1
            except ValueError:
                bot.send_message(message.from_user.id, 'неправильный ввод')

        else:
            bot.send_message(message.from_user.id, 'я вас не понимаю')


bot.polling()
