import mysql.connector


import telebot
bot = telebot.TeleBot('5095876070:AAFUjQKk44Bd4lDHRg01EOMa8sjSYi8qbRg')
from telebot import types






db = mysql.connector.connect(

    host="localhost",
    user='root',
    password="",
    database = "NoteBook"
)

cur = db.cursor()





# Функция для проверки имени на существование
def checkName(isName):
    sql = "SELECT name FROM users"
    cur.execute(sql)
    names = cur.fetchall()
    p = len(names) - 1
    for i in range(len(names)):
        if names[i] == isName:
            return True
        elif names[i] != isName and i == p:
            return False
        else:
            continue



@bot.message_handler(commands=["start"])
def start(message):
    m=f"  Приветик)). Я бот-записная книжка, могу хранить информацию о твоих знакомых, друзьях, родственнииках, а может даже и не твоих." \
      f"\n В общем я могу быть полезным помощником в хранении информации. " \
      f"\n /notebook "
    bot.send_message(message.chat.id, m)



@bot.message_handler(commands=['notebook'])
def prop(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    act = types.KeyboardButton("Блокнот")
    markup.add(act)
    bot.send_message(message.chat.id, 'Если захочешь выполнить какие действия с блокнотом, жми на кнопку, всегда буду рад помочь))) ', reply_markup=markup)


@bot.message_handler(commands=['GiveTheCategory'])
def category(message):
    m = f'1 - Семья; \n 2 - Друзья;\n 3 - Знакомые; \n 4 - Коллеги; \n 5 - Одногруппники; \n 6 - Другое; \n Введи цифру' \


    bot.send_message(message.chat.id, m)


@bot.message_handler(commands=['no'])
def otkaz(message):
    bot.send_message(message.chat.id, 'Как хочешь')


@bot.message_handler(commands=['AddEvent'])
def event(message):
    bot.send_message(message.chat.id, 'Напиши через запятую : "Событие,, `какое-то содержание`, `YYYY.MM.DD`" (Дату указывать в таком формате , как показано в шаблоне).\n(После слово СОБЫТИЕ стоят две запятые, там должно быть имя(необязательно), если его не указать, то событие привяжется к последнему добавленному пользователю)')



@bot.message_handler(content_types=["text"])
def noteBook(message):
    data = message.text.split(',')

    if len(data) == 3:
        try:
            sql = " INSERT INTO users (name, num, adres) VALUES (%s, %s, %s)"
            cur.execute(sql, data)
            db.commit()
            bot.send_message(message.chat.id, 'Контакт успешно добавлен')
            m = f'Хотите присвоить контакту  одну из категорий?(Семья, друзья, знакомые, коллеги, одногруппники, другое) \n'\
                                              f'/GiveTheCategory\n'\
                                              f'/no'
            bot.send_message(message.chat.id, m)
        except Exception:
            txt = "Контакт с таким именем уже существует"
            bot.send_message(message.chat.id, txt)


    elif len(data) == 2:
        data[0] = data[0].lower()
        data[1] = data[1].strip()
        cor = (data[1],)
        checkNameVar = checkName(cor)

        if data[0] == 'delete':
            if checkNameVar == True:
                cor = (data[1],)
                sql = 'DELETE FROM `users` WHERE users.name = %s'
                cur.execute(sql, cor)
                db.commit()
                txt = "Контакт успешно удален"
                bot.send_message(message.chat.id, txt)

            elif checkNameVar == False:
                txt = "Контакта не существует"
                bot.send_message(message.chat.id, txt)

        elif data[0] == 'find':

            if checkNameVar == True:
                cor = (data[1],)
                sql = ' SELECT * FROM `users` WHERE users.name = %s '
                cur.execute(sql, cor)
                users = cur.fetchall()

                for user in users:

                    sql = "SELECT * FROM notes WHERE notes.user_id = %s"
                    cor = (user[0],)
                    cur.execute(sql, cor)
                    notes = cur.fetchall()
                    for note in notes:
                        sql = "SELECT * FROM typeOfRelationShip WHERE typeOfRelationShip.id_user = %s"
                        cor = (user[0],)
                        cur.execute(sql, cor)
                        TORS = cur.fetchall()
                        for TOR in TORS:
                            txt = (
                                f'Имя: {user[1]}  \n  Номер: {user[2]} \n Адрес: {user[3]} \n Событие: {note[2]} \n Дата события: {note[3]} \n {TOR[2]}')

                            bot.send_message(message.chat.id, txt)

            elif checkNameVar == False:
                txt = "Контакта не существует"
                bot.send_message(message.chat.id, txt)

        else:
            txt = "Я не понимаю"
            bot.send_message(message.chat.id, txt)




    elif len(data) == 4:
        data[0] = data[0].lower()
        data[0] = data[0].strip()
        data[1] = data[1].strip()
        data[2] = data[2].strip()
        data[3] = data[3].strip()
        if data[0]=='событие':
            if data[1]=='':
                sql = "SELECT id FROM users WHERE id  =  (SELECT MAX(id) FROM users)"
                cur.execute(sql)
                id = cur.fetchone()
                id = id[0]
                sql = "INSERT INTO notes( user_id, note, date) VALUES (%s, %s, %s)"
                cor = [id, data[2], data[3]]
                cur.execute(sql, cor)
                db.commit()
                bot.send_message(message.chat.id, "ОК. Все готово. ")
            else :
                cor = (data[1],)
                checkNameVar = checkName(cor)
                if checkNameVar == True:

                    sql = 'SELECT id from users WHERE name = %s'
                    cor = (data[1],)
                    cur.execute(sql, cor)
                    id = cur.fetchone()
                    id = id[0]
                    sql = "INSERT INTO notes( user_id, note, date) VALUES (%s, %s, %s)"
                    cor = [id, data[2], data[3]]
                    cur.execute(sql, cor)
                    db.commit()
                    bot.send_message(message.chat.id, "ОК. Все готово. ")


                else:
                    txt = "Контакта не существует"
                    bot.send_message(message.chat.id, txt)


    elif len(data) == 5:
        cor = (data[1],)
        checkNameVar = checkName(cor)
        if checkNameVar == True:
            data[0] = data[0].lower()
            data[1] = data[1].strip()
            data[2] = data[2].strip()
            data[3] = data[3].strip()
            data[4] = data[4].strip()
            sql = "UPDATE users SET users.name = %s, users.num = %s, users.adres = %s WHERE users.name = %s "
            cor = (data[2], data[3], data[4], data[1])
            cur.execute(sql, cor)
            db.commit()
            txt = "Контакт успешно обновлен"
            bot.send_message(message.chat.id, txt)

        elif checkNameVar == False:
            txt = "Контакта не существует"
            bot.send_message(message.chat.id, txt)

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
                sql = "SELECT * FROM notes WHERE notes.user_id = %s"
                cor = (user[0],)
                cur.execute(sql, cor)
                notes = cur.fetchall()
                for note in notes:
                    sql = "SELECT * FROM typeOfRelationShip WHERE typeOfRelationShip.id_user = %s"
                    cor = (user[0],)
                    cur.execute(sql, cor)
                    TORS = cur.fetchall()
                    for TOR in TORS:

                        txt = (f'Имя: {user[1]}  \n  Номер: {user[2]} \n Адрес: {user[3]} \n Событие: {note[2]} \n Дата события: {note[3]} \n {TOR[2]}')

                        bot.send_message(message.chat.id, txt)



        elif message.text.strip()  == '1':
            sql = "SELECT id FROM users WHERE id  =  (SELECT MAX(id) FROM users)"
            cur.execute(sql)
            id = cur.fetchone()
            id = id[0]
            sql = "INSERT INTO typeOfRelationShip( id_user, TOR) VALUES (%s, %s)"
            cor = [id, "Семья"]
            cur.execute(sql, cor)
            db.commit()
            bot.send_message(message.chat.id, "ОК. Все готово. Хочешь добавить какое-нибудь событие к этому человеку?/AddEvent\n/no")

        elif message.text.strip()  == '2':
            sql = "SELECT id FROM users WHERE id  =  (SELECT MAX(id) FROM users)"
            cur.execute(sql)
            id = cur.fetchone()
            id = id[0]
            sql = "INSERT INTO typeOfRelationShip( id_user, TOR) VALUES (%s, %s)"
            cor = [id, "Друзья"]
            cur.execute(sql, cor)
            db.commit()
            bot.send_message(message.chat.id,
                             "ОК. Все готово. Хочешь добавить какое-нибудь событие к этому человеку?/AddEvent\n/no")

        elif message.text.strip()  == '3':
            sql = "SELECT id FROM users WHERE id  =  (SELECT MAX(id) FROM users)"
            cur.execute(sql)
            id = cur.fetchone()
            id = id[0]
            sql = "INSERT INTO typeOfRelationShip( id_user, TOR) VALUES (%s, %s)"
            cor = [id, "Знакомые"]
            cur.execute(sql, cor)
            db.commit()
            bot.send_message(message.chat.id,
                             "ОК. Все готово. Хочешь добавить какое-нибудь событие к этому человеку?/AddEvent\n/no")

        elif message.text.strip()  == '4':
            sql = "SELECT id FROM users WHERE id  =  (SELECT MAX(id) FROM users)"
            cur.execute(sql)
            id = cur.fetchone()
            id = id[0]
            sql = "INSERT INTO typeOfRelationShip( id_user, TOR) VALUES (%s, %s)"
            cor = [id, "Коллеги"]
            cur.execute(sql, cor)
            db.commit()
            bot.send_message(message.chat.id, "ОК. Все готово. Хочешь добавить какое-нибудь событие к этому человеку?/AddEvent\n/no")

        elif message.text.strip()  == '5':
            sql = "SELECT id FROM users WHERE id  =  (SELECT MAX(id) FROM users)"
            cur.execute(sql)
            id = cur.fetchone()
            id = id[0]
            sql = "INSERT INTO typeOfRelationShip( id_user, TOR) VALUES (%s, %s)"
            cor = [id, "Одногруппники"]
            cur.execute(sql, cor)
            db.commit()
            bot.send_message(message.chat.id, "ОК. Все готово. Хочешь добавить какое-нибудь событие к этому человеку?/AddEvent\n/no")

        elif message.text.strip()  == '6':
            sql = "SELECT id FROM users WHERE id  =  (SELECT MAX(id) FROM users)"
            cur.execute(sql)
            id = cur.fetchone()
            id = id[0]
            sql = "INSERT INTO typeOfRelationShip( id_user, TOR) VALUES (%s, %s)"
            cor = [id, "Другое"]
            cur.execute(sql, cor)
            db.commit()
            bot.send_message(message.chat.id,
                             "ОК. Все готово. Хочешь добавить какое-нибудь событие к этому человеку?/AddEvent\n/no")

        else:
            txt = "Я не понимаю"
            bot.send_message(message.chat.id, txt)



bot.polling(none_stop=True)
