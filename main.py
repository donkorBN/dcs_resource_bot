from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Your bot token
TOKEN = '8069191344:AAFWYeQuXct6ZXcvTcajBFd95XzBJCW6y8o'

# List of resources, mapping buttons to file names
resources = {
    'Math PPT': 'math_presentation.pptx',
    'Physics PDF': 'physics_notes.pdf',
    'Chemistry PPT': 'chemistry_intro.pptx'
}

async def welcome(update: Update, context):
    welcome_message = (
        "Hello! Welcome to the Resource Bot.\n\n"
        "You can download various educational resources like PPTs and PDFs here. "
        "Use the /start command to see the list of resources available for download."
    )
    await update.message.reply_text(welcome_message)

async def start(update: Update, context):
    start_message = (

        custom_keyboard = [
        ['/welcome', '/about', '/start']  # Buttons for welcome and about commands
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    
    # Send the message with the keyboard
    await update.message.reply_text(
        "Welcome! Choose an option below:",
        reply_markup=reply_markup
    ))
# Command to display about information
async def about(update: Update, context):
    about_message = (
        "This is a simple bot that allows you to download educational resources.\n\n"
        "It supports multiple resource categories like Math, Science, and more. "
        "The bot is powered by Python and uses SQLite to manage resources."
    )
    await update.message.reply_text(about_message)

 # Define a custom reply keyboard with /welcome and /about
    custom_keyboard = [
        ['/welcome', '/about']  # Buttons for welcome and about commands
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    
    # Send the message with the keyboard
    await update.message.reply_text(
        "Welcome! Choose an option below:",
        reply_markup=reply_markup
    )

# Start command to display buttons
async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton(resource, callback_data=resource) for resource in resources]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a resource to download:", reply_markup=reply_markup)

# Function to handle button presses and send files
async def button(update: Update, context):
    query = update.callback_query
    resource_name = query.data
    
    # Send the appropriate resource
    file_path = resources.get(resource_name)
    if file_path:
        await query.answer()
        with open(file_path, 'rb') as file:
            await context.bot.send_document(chat_id=query.message.chat_id, document=file)
    else:
        await query.answer('Resource not found.')

# Main function to set up the bot
def main():
    # Create an application object with your bot's token
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler('welcome', welcome))  # Welcome command
    application.add_handler(CommandHandler('about', about))  # About command

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
