import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

import api

load_dotenv()

TOKEN = os.getenv('TOKEN')
PORT = int(os.getenv('PORT', 5000))
HEROKU_PATH = os.getenv('HEROKU_PATH')
LOG_GROUP_ID = os.getenv('LOG_GROUP_ID')


# start function
async def start(update: Update, context: CallbackContext) -> None:
    text = 'Hey there! I\'m publibikebot bot and I can do a loooooot of things! \n'
    text += 'Send me /help to see all the things I can do! \n'
    await update.message.reply_text(text)
    return


# help function
async def help_command(update: Update, context: CallbackContext) -> None:
    text = 'Here are the things I can do: \n'
    text += '/start : Start the bot \n'
    text += '/help: Show this message \n'
    text += '/locate <BIKE_ID>: Locate a bike'
    await update.message.reply_text(text)
    return


# locale function
async def locate(update: Update, context: CallbackContext) -> None:
    if ' ' in update.message.text:
        _, id = update.message.text.split(' ', 1)
        await update.message.reply_text(api.locate(id))
    else:
        text = 'Please provide a text to generate a QRCode\n'
        text += 'Example : /qr example.com'
        await update.message.reply_text(text)
    return


# main function
def main() -> None:
    # Create application
    application = Application.builder().token(TOKEN).build()

    # General commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("locate", locate))

    # Start the Bot
    print("Bot starting...")
    if os.environ.get('ENV') == 'DEV':
        application.run_polling()
    elif os.environ.get('ENV') == 'PROD':
        application.run_webhook(listen="0.0.0.0",
                                port=int(PORT),
                                webhook_url=HEROKU_PATH)
    return


if __name__ == '__main__':
    main()
