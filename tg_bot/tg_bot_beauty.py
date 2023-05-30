import pandas as pd
import os
import numpy as np

import json
from sqlalchemy import create_engine

import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.ext.filters import TEXT, PHOTO


def connection_db():
    # Загрузка данных из файла JSON
    with open('credentials.json') as file:
        credentials = json.load(file)

    # Формирование строки подключения
    db_username = credentials['username']
    db_password = credentials['password']
    db_host = 'localhost'  # Или другой хост базы данных
    db_name = 'postgres'  # Имя вашей базы данных
    db_port = '5432'  # Порт базы данных
    connection_string = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

    # Создание объекта Engine для подключения к базе данных
    eng = create_engine(connection_string)

    return eng


engine = connection_db()


def tg_token():
    # Токен ТГ
    # Загрузка данных из файла JSON
    with open('token_tg.json') as file:
        token_json = json.load(file)
    token = token_json['token']

    return token


TELEGRAM_BOT_TOKEN = tg_token()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update: Update, context: CallbackContext):
    welcome_message = (
        """Привет! Я бот "Салоны красоты Кипра" — твой надежный помощник в поиске и записи на услуги красоты на прекрасном острове Кипр!

    🌸 Что я могу для тебя сделать?
    
        Я собрал для тебя все самые лучшие салоны красоты со всего Кипра, чтобы ты мог найти и выбрать именно то, что нужно тебе.
        Я предоставлю тебе удобный способ записи на любую услугу красоты в любом городе Кипра.
         У нас есть специальные услуги и салоны, которые предоставляют широкий спектр услуг, чтобы каждый мог получить качественный уход и стильное преображение.
         
        💅 Как пользоваться ботом?
        
        1️⃣ Отправь мне название услуги, которую ты хочешь получить. Например, маникюр, педикюр, массаж или любую другую услугу, которая тебе интересна, включая мужские услуги, такие как бритье, стрижка и подстригание бороды.
        2️⃣ Укажи город, в котором ты хотел бы получить эту услугу. Например, Лимассол, Пафос, Ларнака и т.д.
        3️⃣ Я предложу тебе список доступных салонов красоты в выбранном городе, где можно получить нужную услугу. Ты сможешь выбрать салон, который предлагает широкий спектр услуг, чтобы получить идеальный результат.
        4️⃣ Выбери удобное для тебя время и запишись на услугу. Я помогу тебе с бронированием, чтобы ты мог насладиться качественным уходом и стильным преображением.
    
        🌟 Пользуйся моими возможностями и наслаждайся красотой и уходом за собой на прекрасном острове Кипр! Если у тебя возникнут вопросы или нужна помощь, просто напиши мне, и я с радостью помогу тебе.
        
        Для записи на услугу выбери интересующую категорию, салон, мастера, дату и время, и я помогу тебе сделать бронь. Будь в курсе акций и специальных предложений, которые доступны в салонах красоты на Кипре.
            
        ✨ Добро пожаловать в мир красоты и релаксации на Кипре, где каждый может получить профессиональный уход и стильное преображение!
        
        Отправь /help, чтобы узнать больше о доступных командах и функциях.
        """
    )

    # Кнопка для помощи
    help_button = InlineKeyboardButton("Помощь", callback_data="help")
    # Кнопка для просмотра доступных услуг
    services_button = InlineKeyboardButton("Услуги", callback_data="services")

    # Создание клавиатуры
    keyboard = [
        [help_button, services_button]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка приветствия и клавиатуры пользователю
    # return context.bot.send_message(chat_id=Update.effective_chat.id, text=welcome_message, reply_markup=reply_markup)
    return update.message.reply_text(text=welcome_message, reply_markup=reply_markup)


def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Обработка команд и сообщений
    application.add_handler(CommandHandler("start", start))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
