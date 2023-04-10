import logging
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup


# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    await update.message.reply_text(
        "Привет. Я справочник по нейросетям. Я могу тебе рассказать много интересного о нейросетях\n"
        "Но сначала давай познакомимся. Напиши, пожалуйста, как тебя зовут")
    return 1


async def first_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    name = update.message.text
    print(name)
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
    await update.message.reply_text("Спасибо за ответ! А теперь смотри, что я знаю о нейросетях")
    reply_markup = markup
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.




async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END



async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def address(update, context):
    await update.message.reply_text(
        "Адрес: г. Москва, ул. Льва Толстого, 16")


async def phone(update, context):
    await update.message.reply_text("Телефон: +7(495)776-3030")


async def site(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


async def work_time(update, context):
    await update.message.reply_text(
        "Время работы: круглосуточно.")

# функция кнопки /start, которая запрашивает имя пользователя и возвращает 1 - состояние беседы
# которое переходит в first_response
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

# Зарегистрируем их в приложении перед
# регистрацией обработчика текстовых сообщений.
# Первым параметром конструктора CommandHandler я
# вляется название команды.

reply_keyboard = [['/address', '/phone'],
                      ['/site', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)







def main():
    # Создаём объект Application.


    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("address", address))
    application.add_handler(CommandHandler("phone", phone))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("work_time", work_time))

    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()
