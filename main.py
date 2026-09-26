# main.py
import threading
import time

from scripts.db import DB_inint, DB_update, DB_select, DB_select_new
from scripts.Yandex_Weathe import receipt_data

from simplevk import Bot, Message
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_GROUPID = os.getenv("BOT_GROUPID")

bot = Bot(BOT_TOKEN, group_id=BOT_GROUPID)

CONDITION_RU = {
    'clear': 'ясно',
    'partly_cloudy': 'малооблачно',
    'cloudy': 'облачно',
    'overcast': 'пасмурно',
    'drizzle': 'морось',
    'light_rain': 'небольшой дождь',
    'rain': 'дождь',
    'moderate_rain': 'умеренный дождь',
    'heavy_rain': 'сильный дождь',
    'showers': 'ливень',
    'wet_snow': 'дождь со снегом',
    'light_snow': 'небольшой снег',
    'snow': 'снег',
    'snow_showers': 'снегопад',
    'blizzard': 'метель',
    'hail': 'град',
    'thunderstorm': 'гроза',
    'thunderstorm_with_rain': 'гроза с дождём',
    'thunderstorm_with_hail': 'гроза с градом',
    'fog': 'туман',
    'smoke': 'дымка',
    'dust': 'пыль',
    'mist': 'дымка',
    'haze': 'мгла',
    'tornado': 'смерч',
    'hurricane': 'ураган',
    'squall': 'шквал',
}

def day_message():
    data = DB_select()
    mes = ""
    print(data)
    for h in data:
        time = h[0]
        temp = h[1]
        state = h[2]
        if time < 10:
            time = "0"+str(time)
        if temp > 0:
            if temp < 10:
                temp = " +"+str(temp)
            else:
                temp = "+"+str(temp)
        mes += f"<{time}:00>  {temp},  {CONDITION_RU[state]}\n"

    return mes

@bot.on.message()
def handler(message):
    text = message.text.strip().lower()
    if text == "/hour":
        h = DB_select_new()
        temp = h[0]
        state = CONDITION_RU[h[1]]
        if temp > 0:
            if temp < 10:
                temp = " +"+str(temp)
            else:
                temp = "+"+str(temp)

        message.answer(f"Сейчас погода: {temp}, {state}")
        return
    if text == "/day":
        message.answer("Прогноз погоды:")
        message.answer(day_message())
        return

    if text == "/help":
        message.answer(
            "Доступные команды:\n"
            "/hour — погода сейчас/\n"
            "/day  — погода на день"
        )
        return

    message.answer(
        "Доступные команды:\n"
        "/hour — погода сейчас/\n"
        "/day  — погода на день"
    )



def bot_run():
    bot.start_listen()

def db_update():
    data = receipt_data("9e55e98f-a439-409f-8bbb-5e7c9ba01c2d")
    DB_update(data)

def update_data():
    while True:
        try:
            db_update()
        except Exception as e:
            print(f"Ошибка БД: {e}")
        time.sleep(3600)


if __name__ == "__main__":
    DB_inint()
    #db_update()

    #threading.Thread(target=update_data, daemon=True, name="DBThread").start()
    bot_run()