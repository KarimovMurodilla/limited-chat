# -*- coding: utf-8 -*-

import re
import asyncio
import logging
import datetime
import pytz

from aiogram import types
from aiogram import executor
from aiogram.dispatcher import filters

from loader import bot, dp, db

GROUP_ID = -1001175586311  # Ваш ID группы

SPAM_TXT = [
    'ООО', 'НДС', 'https://', 'http://', 't.me/', 'Фальш', 'Гарант скам', 'Гарант кидок', 
    'Гарант кидало', 'Ссылка на чат', 'www.', 'OОО', 'Скам чат', 'чат скам', '/start', 
    'https://t.me/', 'YouTu.be', '#экономия_в_магазинах', 'https://t.me', '@lolzteam_garant_bot', 
    'обнал', 'залив', 'scrooge_garantbot', 'эцп', 'covid', 'ковид', 'прийму залив', '🔥 качественная рассылка', 
    'базы', 'оружие', 'фальшей', 'отрисовка', 'сс', 'cc', '@garantbotsa_bot', '@synpro_bot', '@scrooge_garantbot', 
    'лукойл', 'киви', 'qiwi', 'бесплатных курсов', 'открыт набор сотрудников', 'bot', 'устал сидеть без денег', 
    'базу', 'физы', 'сертификат', 'пятёрочке', 'пятерочки', 'ставки', 'ставками', 'договорные матчи', 'договорной матч', 
    '@getgarantbot', '.com', 'https:', '@hermesgarantbot', 'lolz.guru', 'цп', 'elf bar', '@uagarant', 'интим', '@time_m0ney', 
    'бд', 'баз', '👉 налоговая', 'бомбер', 'строки', '@bigautopostbot', 'порно', 'беттинг', 'провожу набор в команду', 
    'sports betting', 'сигарет', 'инвайт в ваш чат', 'ингалятор', 'база', 'спортивных событий', 'спорт событиям', '@sharkgarant1', 
    'гидры', 'гидра', 'хочешь много денег', 'bigautopost', '🔥 реклама в telegram 🔥', '🔥peклaма b telegram🔥', 'pаccылkа вашего объявления', 
    '@worldwidewebshopbot', '1.если принимаете деньги', 'заливаю на карты', 'залог', 'бот:', 'кардингу', 'bот', '🛠️ ‖ frostysmm', '_robot', 
    'продам строчки', '@abyssxgarantbot', 'мегафон', 'only_temki', 'мфо', 'гидрой', 'hydra', 'нарко', 'ramp', 'наркошоп', 'гидру', 
    'договорняк', 'договорняку'
]


@dp.message_handler(content_types = 'text', chat_id = GROUP_ID)
async def delete_links_and_spam_texts(message: types.Message):
    user_id = message.from_user.id
    db.checkUser(user_id)
    db.add_count(user_id)

    if db.get_count(user_id) <= 3:
        if message.entities:
            for entity in message.entities:  # Пройдёмся по всем entities в поисках ссылок
                # url - обычная ссылка, text_link - ссылка, скрытая под текстом
                if entity.type in ["url", "text_link"]:
                    # Мы можем не проверять chat.id, он проверяется ещё в хэндлере
                    await message.delete()

        if any(word in message.text for word in SPAM_TXT):
            print('any')
            await message.delete()

        else:
            regex = (
                r"\w+\n\n"
                r"📩 Связь: @[a-zA-Z0-9_]+\n"
                r"🤖 Гарант: @[a-zA-Z0-9_]+"
                )

            matches = re.search(regex, message.text, re.MULTILINE)

            if not matches:
                print('not match')
                await message.delete()
                await message.answer(
                    "Введите сообщение в формате:\n\n"

                    "Текстовое сообщение\n\n"

                    "📩 Связь: @username\n" 
                    "🤖 Гарант: @LookGarantBot"
                    )

    else:
        moscow_time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y, %m, %d')
        moscow_time = moscow_time.split(',')
        y, m, d = int(moscow_time[0]), int(moscow_time[1]), int(moscow_time[2])
        until_date = datetime.datetime(y, m, d) + datetime.timedelta(days = 1)
        
        db.reset_count(user_id)
        try:
            await bot.restrict_chat_member(
                chat_id = message.chat.id, 
                user_id = message.from_user.id,
                permissions = types.ChatPermissions(
                    can_send_messages = False),
                until_date = until_date
                )
            await message.delete()
            await message.answer(f'@{message.from_user.username}, максимальное количество постов в день 3')
        except:
            pass



async def main(dp):
    logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup = main)
