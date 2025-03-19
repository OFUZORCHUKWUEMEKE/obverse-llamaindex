"""
  Bot Implementations
"""

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from agents.agent import llm
from core.config import config
from repositories.user_repository import create_user,get_user
from models.user import UserSchema


async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_info = update.message.from_user
    telegram_user = update.effective_user # Extract user details
    existing_user = await get_user(str(telegram_user.id))
    if existing_user:
        await update.message.reply_text(
            f"Hello! {user_info.first_name}, Welcome to Obverse\n" 
            f"Obverse is a Stablecoin Payment management agent that helps businesses / Individuals collect fiat payments through links and QRcodes\n"
        )
    else:
        user_data = UserSchema(
          username=telegram_user.username,
          first_name=telegram_user.first_name,
          last_name=telegram_user.last_name,
          telegram_id=str(telegram_user.id)
        )
        user = await create_user(user_data) 
        await update.message.reply_text(
          f"Hello! {user_info.first_name}, Welcome to Obverse\n" 
          f"Obverse is a Stablecoin Payment management agent that helps businesses / Individuals collect fiat payments through links and QRcodes\n" )

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