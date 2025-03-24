"""
  Bot Implementations
"""

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from agents.agent import llm
from core.config import config
from repositories.user_repository import create_user,get_user
from models.user import UserSchema

# Define states for conversation
SELECT_FIELD, UPDATE_VALUE = range(2)


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

async def profile(update:Update,context:ContextTypes.DEFAULT_TYPE):
    """Handles the /profile command and fetches user details from MongoDB."""
    telegram_user = update.effective_user
    user = await get_user(str(telegram_user.id))  # Fetch user from MongoDB

    if user:
        profile_text = (
            f"👤 *Your Profile*\n"
            f"🆔 *Telegram ID:* {user['telegram_id']}\n"
            f"📛 *Username:* {user.get('username', 'N/A')}\n"
            f"📝 *Name:* {user.get('first_name', '')} {user.get('last_name', '')}\n"
            f"🏪 *Merchant Name:* {user.get('merchant_name', 'N/A')}\n"
            # f"💳 *Wallets:* {', '.join(user.get('wallet_addresses', [])) or 'None'}\n"
            f"📊 *Total Transactions:* {user.get('total_transactions', 0)}\n"
        )
    else:
        profile_text = "⚠️ You are not registered yet. Use /start to register."

    await update.message.reply_text(profile_text, parse_mode="Markdown")

async def edit_profile(update:Update,context:ContextTypes.DEFAULT_TYPE):
    """Handles the /edit_profile command and allows users to edit their profile."""
    telegram_user = update.effective_user
    user = await get_user(str(telegram_user.id))

    if not user:
        await update.message.reply_text("⚠️ You are not registered yet. Use /start to register.")
        return ConversationHandler.END
    reply_keyboard = [["Merchant Name","Wallet Addresses"],["Cancel"]]

    await update.message.reply_text(
        "What would you like to update ? Select an Option",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard , one_time_keyboard = True)
    )
    return SELECT_FIELD


async def update_value(update:Update,context:CallbackContext):
    """Update the selected field with the new value"""
    telegram_user = update.effective_user
    field = context.user_data["field"]
    new_value = update.message.text

    if field=="wallet_addresses":
        new_value = new_value.split(",")
    result = await update_user(str(telegram_user.id),{field:new_value})

    if result:
        await update.message.reply_text(f"Your {field.replace('_','')} has been Updated")
    else:
        await update.message.reply_text("Failed to update profile. Pleas try again later")
    return ConversationHandler.END

async def cancel(update:Update,context:CallbackContext)->int:
    """Cancel the profile editing process."""
    await update.message.reply_text("🚫 Profile editing cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


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
    application.add_handler(CommandHandler("profile",profile))

    # Add error handler
    application.add_error_handler(error)

    # Start the bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()