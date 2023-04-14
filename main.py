import logging
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from random import randint
import sqlite3

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)



db = sqlite3.connect('users.db')

cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
    name TEXT,
   age integer);
""")
db.commit()

# функция кнопки /start, которая запрашивает имя пользователя и возвращает 1 - состояние беседы
# которое переходит в first_response
async def start(update, context):
    await update.message.reply_text(
        "Привет. Я справочник по нейросетям. Я могу тебе рассказать много интересного о нейросетях\n"
        "Но сначала давай познакомимся. Напиши, пожалуйста, как тебя зовут")
    return 1


async def first_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    global name
    name = update.message.text
    # print(name)
    await update.message.reply_text(
        f"Приятно познакомиться, {name}! А сколько тебе лет?")
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 2


async def second_response(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    age = update.message.text
    logger.info(age)
    cur.execute("INSERT INTO users(name, age) VALUES(?, ?);",
                (name, age))  # записываем ифнормацию о пользователе
    db.commit()

    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    print(rows)
    await update.message.reply_text("Спасибо за ответ! А теперь смотри, что я знаю о нейросетях",
    reply_markup = markup)
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def openKey(update, context):
    await update.message.reply_text('Смотри, что я знаю о нейросетях',
                                    reply_markup=markup)

async def facts(update, context):
    with open('facts.txt') as f:
        s = f.readlines()
        a = s[randint(0, len(s) - 1)]
    await update.message.reply_text(a)

async def close(update, context):
    await update.message.reply_text('Клавиатура закрыта, если захочешь ее открыть, нажми на команду /open',
                                    reply_markup=ReplyKeyboardRemove())

async def info(update, context):
    await update.message.reply_text('создание',
                                    reply_markup=ReplyKeyboardRemove())

# Зарегистрируем их в приложении перед
# регистрацией обработчика текстовых сообщений.
# Первым параметром конструктора CommandHandler я
# вляется название команды.

reply_keyboard = [['/guide', '/facts'],
                      ['/info', '/close']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )




def main():
    # Создаём объект Application.


    application = Application.builder().token(BOT_TOKEN).build()

    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("guide", guide))
    application.add_handler(CommandHandler("facts", facts))
    application.add_handler(CommandHandler("close", close))
    application.add_handler(CommandHandler("open", openKey))
    application.add_handler(CommandHandler("info", info))

    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()



# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()