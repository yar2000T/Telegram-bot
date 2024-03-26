import random
import telebot
from telebot import types
bot = telebot.TeleBot('7169734819:AAE62OMTmfUuh_IYBOl5LM7EN1U6JsSB0Rc')

print('Бот було запущенно')
def is_blocked(message):
    id = message.from_user.id
    file = open('blocked_users.users', 'r+')
    file_data = file.read()
    if str(id) in file_data:
        return 1
    else:
        return id


@bot.message_handler(commands=['help_ban'])
def ban(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name} ти не можеш користуватися ботом тому що\n'
                                      'тебе заблокував адміністратор.⛔')


@bot.message_handler(commands=['comment'])
def comment(message):
    id = is_blocked(message)
    if id == 1:
        bot.send_message(message.chat.id,
                         f'Вибач {message.from_user.first_name} ,але ти заблокований⛔.\n'
                         'Як що хочеш взнати більше про блокування: /help_ban')
    else:
        x = message.text.lower().split(' ')
        x.remove("/comment")
        comments = ' '.join(x)
        comments_file = open('comments.txt', 'w')
        comments_file.write(str(id) + comments)
        comments_file.close()


@bot.message_handler(commands=['admin'])
def admin_panel(message):
    file = open('admins.txt', 'r+')
    file = file.read()
    if str(message.from_user.id) in file:
        bot.send_message(message.chat,f'З поверненням {message.from_user.first_name}!\n'
                                      'Подивитися відгуки: /comments_view\n'
                                      'Заблокувати когось: /ban ід-користувача')

@bot.message_handler(commands=['comment_view'])
def view(message):
    file = open('admins.txt', 'r+')
    file = file.read()
    if str(message.from_user.id) in file:
        comments_file = open('comments.txt', 'r')
        try:
            bot.send_message(message.chat.id, comments_file.read())
        except:
            bot.send_message(message.chat.id, 'Коментарі пусті')

@bot.message_handler(commands=['ban'])
def ban(message):
    file = open('admins.txt', 'r+')
    file = file.read()
    if str(message.from_user.id) in file:
        x = message.text.lower().split(' ')
        x.remove("/ban")
        file = open('blocked_users.users', 'a')
        file.write('\n'+x[0])
        file.close()
        bot.send_message(message.chat.id, 'Заблоковано успішно')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Доброго дня {message.from_user.first_name},прошу до нашого бота PyGame🎮 .\n'
                                      'Вибрати гру гру🎮: /game\n'
                                      'Довідка❓: /help\n'
                                      'Залишити відгук💬: /comment коментар\n'
                                      'Інформація: /info')

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, f'ID користувача:{message.from_user.id}')
    file = open('admins.txt', 'r+')
    file = file.read()
    if message.from_user.id in file:
        bot.send_message(message.chat.id, 'Права:Адміністратор')
    else:
        bot.send_message(message.chat.id, 'Права:Користувач')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     'Бот створено на базі python і запущенний на серерах replit.\n Cтворено Ярославом👤')

@bot.message_handler(commands=['game'])
def variants(message):
    markup = types.InlineKeyboardMarkup()
    # bot.send_message(message.chat.id, 'Вибери гру:')
    btn1 = types.InlineKeyboardButton('ColdHotGame🧊', callback_data='ColdHotGame')
    btn2 = types.InlineKeyboardButton('Загадки(експерементальна гра)', callback_data='Questions')
    markup.row(btn1, btn2)
    bot.reply_to(message, 'Вибери гру:', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def games(callback):
    if callback.data == 'ColdHotGame':
        bot.edit_message_text('Виберіть складність гри:\n'
                              'Легка🟢:   /easy\n'
                              'Помірна🟡: /medium\n'
                              'Важка🔴:   /hard\n'
                              'Хардкор‼:  /hardcore\n', callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'Questions':
        bot.edit_message_text('Щоб почати гру: /questions', callback.message.chat.id, callback.message.message_id)


@bot.message_handler(commands=['questions'])
def questions(message):
    id = is_blocked(message)
    if id == 1:
        bot.send_message(message.chat.id,
                         f'Вибач {message.from_user.first_name} ,але ти заблокований⛔.\n'
                         'Як що хочеш взнати більше про блокування: /help_ban')
    else:
        questions_list = ['Він здалеку прилітає,\nОболонку чорну має\nТо його надійний щит.\nЗвуть же як?',
                          'Має величезний зріст,\nМає голову і хвіст,\nЦе не тигр, не ракета.\nНатякну вам по секрету – це...',
                          'Сонця й зір це хатка-дім,\nMісяць теж живе на нім.\nУ людей завжди потреба\nДотягнутися до…',
                          'Воду в ріках нагріває,\nМатір-Землю зігріває.\nНам всміхається в віконце\nЧарівне, гаряче…',
                          'Нічного неба оберіг,\nІ схожий бік його на ріг.\nКозак моторний, красний,\nХто ж цей красень ясний?',
                          'Планета блакитна,\nКохана, рідна,\nВона твоя, вона моя,\nІ називається...',
                          'Виблискує величезним хвостом у ночі\nЛине серед зірок в порожнечі,\nВона не зірка, не планета,\nЗагадка Всесвіту – це ...']
        answers = ['метеорит', 'комета', 'неба', 'сонце', 'місяць', 'земля', 'комета']
        bot.send_message(message.chat.id, 'Увага! Питання та відповіді можуть повторюватися🔁.')
        ids = random.randrange(0, len(questions_list))
        bot.send_message(message.chat.id, questions_list[ids])

        @bot.message_handler(func=lambda message_: True)
        def _answer_(message, last_message='hi', answer=answers[ids]):
            if last_message != message.text.lower:
                last_message = message.text
                if message.text.lower() == str(answer):
                    bot.send_message(message.chat.id, f'Правильно🥳🏅🏹')
                else:
                    bot.send_message(message.chat.id, f'Неправильно, правильна відповідь:{answers[ids]}')


@bot.message_handler(commands=['easy'])
def easy(message):
    id = is_blocked(message)
    if id == 1:
        bot.send_message(message.chat.id,
                         f'Вибач {message.from_user.first_name} ,але ти заблокований⛔.\n'
                         'Як що хочеш взнати більше про блокування: /help_ban')
    else:
        number = random.randrange(0, 10)
        bot.send_message(message.chat.id, '🏁 Гра починається!\n'
                                          'Загадане ціле число від 1 до 10 🤐\n'
                                          'Відгадай його якнайшвидше 🚀\n')

        @bot.message_handler(func=lambda message: True)
        def messages(message, last_message='hi'):
            if last_message != message.text:
                last_message = message.text
                if int(message.text) == int(number):
                    bot.send_message(message.chat.id, f'Це воно🥳🏅! Ви знайшли число {message.text}🏹')
                else:
                    numberss = int(abs(number - int(message.text)))
                    if numberss > 7:
                        bot.send_message(message.chat.id, 'Прохолодно❄')
                    elif numberss > 4 < 7:
                        bot.send_message(message.chat.id, 'Тепло🌡')
                    elif numberss > 2 < 4:
                        bot.send_message(message.chat.id, 'Гаряче🔥')
                    elif numberss > 0 < 2:
                        bot.send_message(message.chat.id, 'Вулкан!')


@bot.message_handler(commands=['medium'])
def medium(message):
    id = is_blocked(message)
    if id == 1:
        bot.send_message(message.chat.id,
                         f'Вибач {message.from_user.first_name} ,але ти заблокований⛔.\n'
                         'Як що хочеш взнати більше про блокування: /help_ban')
    else:
        number = random.randrange(0, 100)
        bot.send_message(message.chat.id, '🏁 Гра починається!\n'
                                          'Загадане ціле число від 1 до 100 🤐\n'
                                          'Відгадай його якнайшвидше 🚀\n')

        @bot.message_handler(func=lambda message: True)
        def messages(message, last_message='hi'):
            if last_message != message.text:
                last_message = message.text
                if int(message.text) == int(number):
                    bot.send_message(message.chat.id, f'Це воно! Ви знайшли число {message.text}🏹')
                else:
                    numberss = int(abs(number - int(message.text)))
                    if numberss > 70:
                        bot.send_message(message.chat.id, 'Крига❄❄')
                    elif numberss > 50 < 70:
                        bot.send_message(message.chat.id, 'Холодно❄')
                    elif numberss > 25 < 50:
                        bot.send_message(message.chat.id, 'Тепло🌡')
                    elif numberss > 10 < 25:
                        bot.send_message(message.chat.id, 'Гаряче🔥')
                    elif numberss > 0 < 10:
                        bot.send_message(message.chat.id, 'Вулкан!🌋')


@bot.message_handler(commands=['hard'])
def hard(message):
    id = is_blocked(message)
    if id == 1:
        bot.send_message(message.chat.id,
                         f'Вибач {message.from_user.first_name} ,але ти заблокований⛔.\n'
                         'Як що хочеш взнати більше про блокування: /help_ban')
    else:
        number = random.randrange(0, 500)
        bot.send_message(message.chat.id, '🏁 Гра починається!\n'
                                          'Загадане ціле число від 1 до 500 🤐\n'
                                          'Відгадай його якнайшвидше 🚀\n')

        @bot.message_handler(func=lambda message: True)
        def messages(message, last_message='hi'):
            if last_message != message.text:
                last_message = message.text
                if int(message.text) == int(number):
                    bot.send_message(message.chat.id, f'Це воно! Ви знайшли число {message.text}🏹')
                else:
                    numberss = int(abs(number - int(message.text)))
                    if numberss > 400:
                        bot.send_message(message.chat.id, 'Крига❄❄')
                    elif numberss > 300 < 400:
                        bot.send_message(message.chat.id, 'Холодно❄')
                    elif numberss > 200 < 300:
                        bot.send_message(message.chat.id, 'Тепло🌡')
                    elif numberss > 100 < 200:
                        bot.send_message(message.chat.id, 'Тепліше')
                    elif numberss > 10 < 200:
                        bot.send_message(message.chat.id, 'Гаряче🔥')
                    elif numberss > 0 < 10:
                        bot.send_message(message.chat.id, 'Вулкан!🌋')


@bot.message_handler(commands=['hardcode'])
def hardcore(message):
    id = is_blocked(message)
    if id == 1:
        bot.send_message(message.chat.id,
                         f'Вибач {message.from_user.first_name} ,але ти заблокований⛔.\n'
                         'Як що хочеш взнати більше про блокування: /help_ban')
    else:
        number = random.randrange(0, 1000)
        bot.send_message(message.chat.id, '🏁 Гра починається!\n'
                                          'Загадане ціле число від 1 до 1000 🤐\n'
                                          'Відгадай його якнайшвидше 🚀\n')

        @bot.message_handler(func=lambda message: True)
        def messages(message, last_message='hi'):
            if last_message != message.text:
                last_message = message.text
                if int(message.text) == int(number):
                    bot.send_message(message.chat.id, f'Це воно! Ви знайшли число {message.text}🏹')
                else:
                    numberss = int(abs(number - int(message.text)))
                    if numberss > 700:
                        bot.send_message(message.chat.id, 'Антарктида❄❄')
                    elif numberss > 500 < 700:
                        bot.send_message(message.chat.id, 'Крига❄')
                    elif numberss > 300 < 500:
                        bot.send_message(message.chat.id, 'Холодно❄')
                    elif numberss > 200 < 300:
                        bot.send_message(message.chat.id, 'Тепло🌡')
                    elif numberss > 100 < 200:
                        bot.send_message(message.chat.id, 'Тепліше')
                    elif numberss > 10 < 100:
                        bot.send_message(message.chat.id, 'Гаряче🔥')
                    elif numberss > 0 < 10:
                        bot.send_message(message.chat.id, 'Вулкан!🌋')


bot.infinity_polling()
