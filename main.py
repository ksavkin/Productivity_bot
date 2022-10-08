from sqlite3 import Time
import telebot
from telebot import types
import time

bot = telebot.TeleBot("5796025327:AAGmNucofDgGzNLKwvdoOndVaufaIxX3vvY")

count_button = 0
list_tasks = [] # задачи на день
flag = False # флаг, показывающий назвал ли пользователь свои задачи
string_name_tasks = ""
list_name_tasks = []
count = 0 # count для того чтобы один раз вводить время


class Task:
    def __init__(self, name_of_task, importance, urgency, duration):
        self.name_of_task = name_of_task
        self.importance = importance
        self.urgency = urgency
        self.duration = duration


class TimeTable:
    def __init__(self, start_time=None, finish_time=None, list_tasks=None):
        self.start_time = start_time
        self.finish_time = finish_time
        self.list_tasks = list_tasks

    def clean(self):
        self.list_tasks = []

    def delete_task(self, name_of_task):
        self.list_tasks.remove(name_of_task)

    def add_task(self, name_of_task, importance, urgency, duration):
        task = Task(name_of_task, importance, urgency, duration)
        self.list_tasks.append(task)


time_table = TimeTable()


# защита от лохов
@bot.message_handler(content_types=['audio', 'document', 'sticker', 'video', 'voice', 'contact', 'first_name', 'last_name'
                                    'id', 'username', 'forward_from', 'video_note', 'game', 'photo', 'dice', 'poll', 'location'
                                    'venue', 'forward_from_chat', 'forward_from_message_id', 'forward_signature', 'forward_date'
                                    'is_automatic_forward', 'reply_to_message', 'animation'])
def fefefe(message):
    bot.send_message(message.from_user.id, 'не надо дядя')


def buttons_func(message):
    global string_name_tasks
    global time_table
    # обработка кнопок
    if message.text == "Вывести мои задачи":
        bot.send_message(message.from_user.id, "задачи: " + string_name_tasks)
    elif message.text == "Измнеить список задач":
        bot.send_message(message.from_user.id, "пошел нахер пиши изначально правильно")
    else: # только если всего 3 кнопки иначе elif
        time_table.list_tasks = []
        string_name_tasks = ""
        bot.send_message(message.from_user.id, "готово")
        bot.send_message(message.from_user.id, "на данный момент у вас нет задач")


# начальная фразочка
@bot.message_handler(commands=['start'])
def start(message):
    global list_tasks
    global count_button
    list_tasks = []
    if message.text == '/start':
        count_button = 0
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

    elif message.text == "Вывести мои задачи" or message.text == "Измнеить список задач" or message.text == "Очистить список задач":
        buttons_func(message)
    # создание кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вывести мои задачи")
    btn2 = types.KeyboardButton("Измнеить список задач")
    btn3 = types.KeyboardButton("Очистить список задач")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Теперь можно использовать кнопки для хз чего".format(message.from_user), reply_markup=markup)
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
        bot.send_message(call.message.chat.id, text='Тогда до скорой встречи',
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def time_function(message):
    global count
    if message.text == "Вывести мои задачи" or message.text == "Измнеить список задач" or message.text == "Очистить список задач":
        buttons_func(message)
    elif count >= 1:
        bot.register_next_step_handler(message, tasks_function)

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
        if (semicolon == 1) and (colon == 2) and count == 0:
            semicolon = 0
            colon = 0
            count += 1
            global flag
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
                print(time_table.start_time, time_table.finish_time, time_table.list_tasks)
                bot.send_message(message.from_user.id, 'введите список задач в формате: название задачи срочность(от 1 до 10) (важность(от 1 до 10) продолжительность(в минутах) пример: поесть 10 8 15; ауджимания 10 10 90')
                bot.register_next_step_handler(message, tasks_function)

            except ValueError:
                bot.send_message(message.from_user.id, 'говно ввел')

        else:
            bot.send_message(message.from_user.id, 'я вас не понимаю')


@bot.message_handler(content_types=['text'])
def tasks_function(message):
    global list_tasks
    global time_table
    global string_name_tasks
    global list_name_tasks

    if message.text == "Вывести мои задачи" or message.text == "Измнеить список задач" or message.text == "Очистить список задач":
        buttons_func(message)

    else:
        if ";" in message.text:
            # тупая проверка присутствует ли больше 1 задачи + что это не кнопка
            message_new = message.text.split("; ")
            for i in message_new:
                sp = i.split(" ") # начинаем разбираться где название задачи/важность/срочность/длительность
                name_of_task = sp[0]
                urgency = sp[1]
                importance = sp[2]
                duration = sp[3]
                task = Task(name_of_task, importance, urgency, duration)
                list_tasks.append(task)
                time_table.list_tasks = list_tasks

        else:
            sp = message.text.split(" ")
            name_of_task = sp[0]
            urgency = sp[1]
            importance = sp[2]
            duration = sp[3]
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
        bot.send_message(message.from_user.id, "вы добавили следующие задачи: " + string_name_tasks)


bot.polling()
