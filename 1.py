import telebot
import sqlite3
import requests
import json
from telebot import types

bot = telebot.TeleBot('6522037084:AAGD8NfgollzmS49aUMBGywU40Av_cYxWPg')


@bot.message_handler(commands=['start'])
def privet(massage):
    bot.send_message(massage.chat.id,
                     '<b>Здравствуйте</b>, вас приветсвует Бот-расписание!',
                     parse_mode='html')
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users( id INTEGER, id_git INTEGER)""")

    connect.commit()

    people_id = massage.chat.id
    cursor.execute(f"SELECT id FROM users WHERE id = {people_id}")
    data = cursor.fetchone()
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton('Расписание', callback_data= 'shadule')
    item2 = types.InlineKeyboardButton('Я администратор', callback_data='admin')
    item20 = types.InlineKeyboardButton('Выйти из моего аккаунта', callback_data='delete')
    markup.add(item, item2, item20)
    my_name = " "
    my_group = "ПИ-231 "
    def save_name(message):
        my_name = message.text
        bot.send_message(message.chat.id, "Сохранил!")
    if data is None:
        users_list = [massage.chat.id]
        cursor.execute("INSERT INTO users VALUES(?);", users_list)
        connect.commit()
        bot.send_message(massage.chat.id, "Необходима авторизация")
        sent = bot.send_message(message.chat.id, "Введите свое имя и фамилию :")
        bot.register_next_step_handler(sent, save_name)
        headers = {"Security-Token": "almostsecure!"}
        data2 = {"chat_id": massage.chat.id, "name": my_name, "group": my_group}
        response = requests.post("/start_register", headers=headers, data=data2)
        API_Data = response.json()
        if response.status_code == 200:
            bot.send_message(massage.chat.id, API_Data["url"])
            """id_git2 = получение id github
            cursor.execute(f"SELECT id_git FROM users WHERE id_git = {id_git2}")"""
            bot.send_message(massage.chat.id, "Вы успешно вошли", reply_markup=markup)
        else:
            bot.send_message(massage.chat.id, "Произошла ошибка. Повторите еще раз.")
    else:
        bot.send_message(massage.chat.id, "Вы успешно вошли", reply_markup= markup)


@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'shadule':
            headers1 = {"Security-Token": "almostsecure!"}
            data2 = {"chat_id": massage.chat.id}
            response = requests.post("/get_schedule", headers=headers1, data=data2)
            otvet = response.text
            headers2 = {"Security-Token": "sdfdslfs"}
            response2 = requests.get("/topsecretvalue", headers=headers2, data=otvet)
            res2 = response2.json()
            bot.send_message(massage.chat.id, res2)
        if call.data == 'admin':
            headers3 = {"Security-Token": "что-то"}
            data3 = {"chat_id": massage.chat.id}
            response3 = requests.post("/start_admin_session", headers=headers3, data=data3)
            res1 = response3.text
            headers4 = {"Security-Token": "application/json"}
            data4 = {"chat_id": massage.chat.id, "JWT_token": res1}
            response4 = requests.post("/start_admin_session", headers=headers4, data=data4)
            gg = response4.text
            if response4.status_code == 200:
                bot.send_message(massage.chat.id, gg["url"])
        if call.data == 'delete':
            def delete2(message):
                connect = sqlite3.connect('users.db')
                cursor = connect.cursor()
                people_id = call.message.chat.id
                cursor.execute(f"DELETE FROM users WHERE id = {people_id}")
                bot.send_message(call.message.chat.id, "Вы успешно вышли")
            delete2(call.message)



@bot.message_handler(commands=['help'])
def privet(massage):
    bot.send_message(massage.chat.id, massage)


bot.polling(none_stop = True, interval = 0)
