"""
  Bot Implementations
"""

import os
from telegram import Update,ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler,CallbackContext, CallbackQueryHandler
# from agents.agent import llm
from core.config import config
from repositories.user_repository import create_user,get_user,update_user
from repositories.payment_repository import create_payments
from models.user import UserSchema,UpdateUser
from utils.utils import generate_reference
from models.payment import PaymentSchema

# Define states for conversation
SELECT_FIELD, UPDATE_VALUE = range(2)
SELECTING_OPTION, WAITING_FOR_INPUT = range(2)

TITLE,DESCRIPTION,LOGO_URL,AMOUNT,DETAILS,CONFIRM= range(6)


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

async def edit_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Merchant Name", callback_data="merchant_name")],
        [InlineKeyboardButton("Wallet Address", callback_data="wallet_address")],
        [InlineKeyboardButton("Logo URL", callback_data="logo_url")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)
    return SELECTING_OPTION

# Function to handle user selection
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    selected_option = query.data
    context.user_data["selected_option"] = selected_option

    # Ask the user to enter the value
    # await query.message.(f"Please enter your {selected_option.replace('_', ' ')}:")
    await query.edit_message_text(f"Please enter your {selected_option.replace('_', ' ')}:")

    return WAITING_FOR_INPUT  # Move to next state

# Handle user input
async def user_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    selected_option = context.user_data.get("selected_option", "Unknown Field")
    update_data ={}

    # Process input (store, send, etc.)
    response = f"✅ You entered '{user_text}' for {selected_option.replace('_', ' ')}."
    await update.message.reply_text(response)

    if selected_option == "merchant_name":
        update_data = {"merchant_name": user_text}
    elif selected_option == "wallet_address":
        update_data = {"$push": {"wallet_addresses": user_text}} 
    elif selected_option == "logo_url":
        update_data = {"logo_url": user_text}
    
    if update_data:
        await update_user(str(update.effective_user.id),UpdateUser(**update_data))
    response = f"✅ Updated *{selected_option.replace('_', ' ')}* with:\n\n`{user_text}`"
    await update.message.reply_text(response, parse_mode="Markdown")

    return ConversationHandler.END  # End conversation

# Cancel command (if user wants to exit)
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END

async def create_payment(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please Enter the title of your payment")
    return TITLE

async def get_title(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data['title'] = update.message.text
    await update.message.reply_text("Enter the description of the payment:")
    return DESCRIPTION

async def get_description(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data['description'] = update.message.text
    await update.message.reply_text("Enter the logo url of the payment:")
    return LOGO_URL

async def get_logo_url(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data['logo_url'] = update.message.text
    await update.message.reply_text("Enter the amount of the payment: eg(10 , 20 ,10),i.e we only support USDT")
    return AMOUNT

async def get_amount(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data['amount'] = update.message.text
    await update.message.reply_text("Enter details you require your users to fill before making payments")
    return DETAILS

async def get_details(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data["details"] = update.message.text.split(',')
    payment_info = (f"Payment Details:\n"
                    f"Title: {context.user_data['title']}\n"
                    f"Description: {context.user_data['description']}\n"
                    f"Logo URL: {context.user_data['logo_url']}\n"
                    f"Amount: {context.user_data['amount']}\n"
                    f"Details: {', '.join(context.user_data['details'])}"
                    )
    keyboard = [
        [InlineKeyboardButton("Confirm", callback_data="confirm")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(payment_info, reply_markup=reply_markup)
    return CONFIRM

async def confirm(update: Update,  context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    if query.data == "confirm":
        await query.edit_message_text("Creating Payment Link... ✅")
        amount = context.user_data["amount"]
        logo_url = context.user_data["logo_url"]
        title = context.user_data["title"]
        description = context.user_data["description"]
        reference = generate_reference()
        details = context.user_data["details"]
        payment_data = PaymentSchema(
            amount=amount,
            logo_url=logo_url,
            title=title,
            description=description,
            user_id=str(query.from_user.id),
            reference=reference,
            details=details
        )
        payment = await create_payments(payment_data)
        payment_link = "https://paypal.me/yourusername/10"
        # image_url=f"https://pay.obverse.com/payment/{payment['reference']}"
        image_url = "http://picsum.photos/200/200"
        # await query.edit_message_text(f"Payment Link Created: https://pay.obverse.com/payment/{payment['reference']}")
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
        photo=image_url,
        caption=f"Here’s the payment link: [{payment_link}]({payment_link})",
        parse_mode='Markdown'  # Makes the link clickable
        )

        return ConversationHandler.END
    else:
        await query.edit_message_text("Payment canceled. ❌")
        return ConversationHandler.END


# Define a handler for echoing text messages
# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     response = llm.complete(update.message.text)
#     await update.message.reply_text(response.text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Available Commands\n" +
        "Use /start to register.\n" +
        "/profile – View your account details.\n" +
        "/edit_profile – Update your account details.\n" +
        "/help – Get a list of available commands and how to use them.\n" +
        "/create_payment – Generate a payment request with ease.\n" +
        "/invoice – Manage and track your invoices.\n" +
        "/dashboard – Access an overview of your transactions and earnings.\n"+
        "/agent - Chat with Agents"
        )

# Define an error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(config.TELEGRAM_BOT).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler("help",help))
    application.add_handler(CommandHandler("profile",profile))
     # Define conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("edit_profile", edit_profile)],
        states={
            SELECTING_OPTION: [CallbackQueryHandler(button_handler)],
            WAITING_FOR_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_input_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    payment_handler = ConversationHandler(
        entry_points=[CommandHandler("create_payment", create_payment)],
        states={
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_description)],
            LOGO_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_logo_url)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)],
            DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_details)],
            CONFIRM: [CallbackQueryHandler(confirm)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(payment_handler)

    # Add error handler
    application.add_error_handler(error)

    # Start the bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()