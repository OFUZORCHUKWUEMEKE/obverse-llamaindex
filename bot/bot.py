"""
  Bot Implementations
"""

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from agents.agent import llm
from core.config import config


async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f"Hello! {user.first_name}, Welcome to Obverse\n" 
        f"Obverse is a Stablecoin Payment management agent that helps businesses / Individuals collect fiat payments through links and QRcodes\n"
    )

# Define a handler for echoing text messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = llm.complete(update.message.text)
    await update.message.reply_text(response.text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a help message!")

async def signup(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await print("Signup")

# Define an error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(config.TELEGRAM_BOT).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler("help",help))

    # Add error handler
    application.add_error_handler(error)

    # Start the bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()