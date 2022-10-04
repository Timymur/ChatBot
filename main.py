import mysql.connector


import telebot
bot = telebot.TeleBot('5095876070:AAFUjQKk44Bd4lDHRg01EOMa8sjSYi8qbRg')
from telebot import types



mydb = mysql.connector.connect(

    host = "localhost",
    user = 'root',
    password = ""
)
myCur = mydb.cursor()
sql = "CREATE DATABASE IF NOT EXISTS NoteBook"
myCur.execute(sql)


db = mysql.connector.connect(

    host="localhost",
    user='root',
    password="",
    database = "NoteBook"
)

cur = db.cursor()

cur.execute(''' CREATE TABLE IF NOT EXISTS users (
    id int auto_increment primary key,
    name varchar(30) UNIQUE ,  
    num varchar(20),
    adres TEXT
) ''')





@bot.message_handler(commands=["start"])
def start(message):
    m=f"  Приветик)). Я бот-записная книжка, могу хранить информацию о твоих знакомых, друзьях, родственнииках, а может даже и не твоих.\n В общем я могу быть полезным помощником в хранении информации. \n /notebook "
    bot.send_message(message.chat.id, m)






@bot.message_handler(commands=['notebook'])
def prop(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    act = types.KeyboardButton("Блокнот")
    markup.add(act)
    bot.send_message(message.chat.id, 'Если захочешь выполнить какие действия с блокнотом, жми на кнопку, всегда буду рад помочь))) ', reply_markup=markup)



@bot.message_handler(content_types=["text"])
def noteBook(message):
    data = message.text.split(',')
    if len(data) == 3:
        sql = " INSERT INTO users (name, num, adres) VALUES (%s, %s, %s)"
        cur.execute(sql, data)
        db.commit()
        bot.send_message(message.chat.id, 'Контакт успешно добавлен')



    else:

        if message.text == 'Блокнот':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            ad = types.KeyboardButton("Добавить контакт")
            de = types.KeyboardButton("Удалить контакт")
            ch = types.KeyboardButton("Изменить контакт")
            sh = types.KeyboardButton("Поиск контакта")
            al = types.KeyboardButton("Показать все записи")
            markup.add(ad, de, ch, sh, al)
            bot.send_message(message.chat.id, 'Выбери, что хочешь сделать' ,reply_markup=markup)

        elif message.text == 'Поиск контакта':
            txt = "Напиши: find, имя контакта"
            bot.send_message(message.chat.id, txt)

        elif message.text == 'Добавить контакт':
            txt = "Напиши через запятую имя, номер, адрес нового контакта\n(при указании адреса не используй запятые)"
            bot.send_message(message.chat.id, txt)

        elif message.text == 'Удалить контакт':
            txt = "Напиши: delete, имя контакта"
            bot.send_message(message.chat.id, txt)

        elif message.text == 'Изменить контакт':
            txt = "Напиши через запятую: update, имя контакта, новое имя, новый номер, новый адрес"
            bot.send_message(message.chat.id, txt)

        elif message.text == 'Показать все записи':
            cur.execute('SELECT * FROM users')
            users = cur.fetchall()
            for user in users:
                txt = (f'Имя: {user[1]}  |  Номер: {user[2]} | Адрес: {user[3]}')
                bot.send_message(message.chat.id, txt)

    if len(data) == 2:
        data[0] = data[0].lower()
        data[1] = data[1].strip()
        if data[0] == 'delete':
            cor = (data[1],)
            sql = 'DELETE FROM `users` WHERE users.name = %s'
            cur.execute(sql, cor)
            db.commit()
            txt = "Контакт успешно удален"
            bot.send_message(message.chat.id, txt)

        if data[0] == 'find':
            cor = (data[1], data[1], data[1] )
            sql = ' SELECT * FROM `users` WHERE users.name = %s OR users.num = %s OR users.adres = %s '
            cur.execute(sql, cor)
            users = cur.fetchall()
            for user in users:
                contact = (f'Имя: {user[1]}  \n  Номер: {user[2]} \n Адрес: {user[3]} ')
                bot.send_message(message.chat.id, contact)

    if len(data) == 5:
        data[0] = data[0].lower()
        data[1] = data[1].strip()
        data[2] = data[2].strip()
        data[3] = data[3].strip()
        data[4] = data[4].strip()
        sql = "UPDATE users SET users.name = %s, users.num = %s, users.adres = %s WHERE users.name = %s "
        cor = (data[2], data[3], data[4], data[1]  )
        cur.execute(sql, cor)
        db.commit()
        txt = "Контакт успешно обновлен"
        bot.send_message(message.chat.id, txt)













bot.polling(none_stop=True)
