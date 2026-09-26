from simplevk import Bot, Message
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_GROUPID = os.getenv("BOT_GROUPID")

bot = Bot(BOT_TOKEN, group_id=BOT_GROUPID)


@bot.on.message()
def handler(message):
    text = message.text.strip().lower()

    if text == "/ping":
        message.answer("Pong!")
        return

    if text == "/help":
        message.answer(
            "Доступные команды:\n"
            "/ping — проверить бота\n"
            "/help — показать помощь"
        )
        return

    message.answer(f"Вы сказали: {message.text}")

def bot_run():
    bot.start_listen()

if __name__ == "__main__":
   bot_run()