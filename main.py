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
    await update.message.reply_text('Это бот о нейросетях был разработан учениками второго курса Лицее Академии Яндекса Лионой Прохоренко и Машей Лопаткиной.\n'
'В ходе общения с нашим ботом вы можете воспользоваться несколькими функциями:\n'
'/start - команда, начинающая диалог заново\n'
'/guide - команда, вызывающая сборник ссылок на статьи о нейросетях\n'
'/facts - команда, отправляющая случайный факт из истории разработки нейросетей\n'
'/close - команда, позволяющая закрыть клавиатуру с кнопками, когда вы вызываете эту функцию\n'
'/open - команда, позволяющая открыть клавиатуру, если вы закрыли её функцией /close\n'
'/info - команда, с помощью которой вы можете узнать о возможностях нашего бота',
                                    reply_markup=ReplyKeyboardRemove())

# Зарегистрируем их в приложении перед
# регистрацией обработчика текстовых сообщений.
# Первым параметром конструктора CommandHandler я
# вляется название команды.


async def guide(update, context):
    await update.message.reply_text('/neuro - что такое нейросети?\n'
                                    '/use - где используются нейросети\n' 
                                    '/future - будущее нейросетей\n'
                                    '/creation - создание и обучение нейросетей\n' 
                                    '/lib - библиотеки для работы с нейросетями'
                                    )


async def neuro(update, context):
    # context.bot.send_photo(photo=open('images/neuro.jpeg'))
    await update.message.reply_photo(photo='https://disk.yandex.ru/i/S_N6htapspOHlg',
                                    caption='Нейронные сети - это математические модели, которые имитируют'
                                    'работу человеческого мозга '
                                    'и способны решать разнообразные задачи.\n'
                                    ' Они состоят из множества связанных нейронов и могут быть построены в различных '
                                    'архитектурах. Для обучения нейронных сетей требуется большой объем данных и '
                                    'мощные вычислительные ресурсы.\n'
                                    ' Нейронные сети широко применяются в различных областях, '
                                    'включая медицину, финансы, автоматический перевод, игры и т.д'
                                    )


async def use(update, context):
    await update.message.reply_photo(photo='https://disk.yandex.ru/i/H5uXVXdPvRk8qQ',
                                     caption='Нейросети в настоящее время используются во многих областях, включая:\n'
                                    'Компьютерное зрение: распознавание образов, детектирование объектов на изображениях и видео.\n'
                                    'Распознавание речи: преобразование речи в текст и наоборот, а также контроль голосовых помощников.\n'
                                    'Машинный перевод: автоматический перевод текста с одного языка на другой.\n'
                                    'Рекомендательные системы: предсказание пользовательских предпочтений и рекомендация контента, товаров или услуг.\n'
                                    'Автономная навигация: управление беспилотными транспортными средствами и роботами.\n'
                                    'Биоинформатика: анализ генетических данных и диагностика заболеваний.\n'
                                    'Финансы: прогнозирование цен на акции и валюты, анализ рисков и оптимизация портфеля инвестиций.\n'
                                    'Игровая индустрия: создание искусственного интеллекта для компьютерных игр и обучения ботов.'
                                    )


async def future(update, context):
    await update.message.reply_photo(photo='https://disk.yandex.ru/i/5iH2WolZCPmhYA',
                                     caption='Нейросети имеют огромный потенциал для развития и будут продолжать применяться во многих областях, '
                                    'таких как медицина, финансы, транспорт, обработка естественного языка и игровая индустрия.\n'
                                    ' Ожидается, что с развитием технологий и увеличением доступности данных, нейросети будут становиться'
                                    ' все более точными и эффективными.\n Также предполагается, что нейросети будут использоваться для решения'
                                    ' более сложных задач, таких как создание искусственной жизни, обучение роботов и даже создание '
                                    'искусственного сознания.\n Однако, вместе с возможностями нейросетей, существуют и этические и '
                                    'социальные вопросы, связанные с использованием этих технологий, которые будут требовать внимательного '
                                    'рассмотрения в будущем.'
                                    )


async def creation(update, context):
    await update.message.reply_photo(photo='https://disk.yandex.ru/i/C_alJEPYfj02Ig',
                                     caption='Для создания и обучения нейросети нужно выполнить несколько шагов:'
                                    '1. Определить задачу, которую нужно решить, например, распознавание цифр на изображениях.\n'
                                    '2. Подготовить данные для обучения нейросети, например, набор изображений цифр и соответствующих им меток'
                                    '(это может быть выполнено вручную или с помощью программного обеспечения).'
                                    '3. Выбрать архитектуру нейросети, например, многослойный персептрон, который состоит '
                                    'из нескольких слоев нейронов и может быть использован для распознавания образов.\n'
                                    '4. Обучить нейросеть на подготовленных данных, используя алгоритм обратного распространения ошибки,'
                                    'который позволяет оптимизировать веса нейронов для более точного решения задачи.\n'
                                    '5. Протестировать нейросеть на тестовых данных, которые не были использованы для обучения,'
                                    'чтобы оценить ее точность и убедиться, что она может решать задачу правильно.\n'
                                    '6. Использовать нейросеть для решения задачи в реальном мире, например, для распознавания цифр на изображениях в приложении для мобильного телефона.'
                                                                            )

async def lib(update, context):
    await update.message.reply_photo(photo='https://disk.yandex.ru/i/dVM9w7C1WSom7Q',
                                     caption='Наиболее популярных библиотек для создания нейросетей на Python:'
                                    'TensorFlow - открытая библиотека для глубокого обучения, используемая для создания'
                                    'и обучения нейросетей на больших объемах данных.'
                                    'Keras - высокоуровневая библиотека для создания нейросетей, которая '
                                    'облегчает процесс создания и обучения нейросетей благодаря своей простоте и интуитивно понятному интерфейсу.'
                                    'PyTorch - библиотека для глубокого обучения, которая позволяет создавать и обучать '
                                    'нейросети на основе динамического графа вычислений.'
                                    'Scikit-learn - библиотека машинного обучения, которая включает в себя модули для классификации, '
                                    'регрессии, кластеризации и других задач.'
                                    'Theano - библиотека для глубокого обучения, которая позволяет создавать и обучать нейросети на GPU.'
                                    )


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
    application.add_handler(CommandHandler("guide", guide))
    application.add_handler(CommandHandler("facts", facts))
    application.add_handler(CommandHandler("close", close))
    application.add_handler(CommandHandler("open", openKey))
    application.add_handler(CommandHandler("info", info))

    application.add_handler(CommandHandler("neuro", neuro))
    application.add_handler(CommandHandler("use", use))
    application.add_handler(CommandHandler("future", future))
    application.add_handler(CommandHandler("creation", creation))
    application.add_handler(CommandHandler("lib", lib))
    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()



# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()