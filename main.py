from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Your bot token
TOKEN = '8069191344:AAFWYeQuXct6ZXcvTcajBFd95XzBJCW6y8o'

# List of resources, mapping buttons to file names
resources = {
    'Math PPT': 'math_presentation.pptx',
    'Physics PDF': 'physics_notes.pdf',
    'Chemistry PPT': 'chemistry_intro.pptx'
}

# Start command to display buttons
def start(update: Update, context):
    keyboard = [[InlineKeyboardButton(resource, callback_data=resource) for resource in resources]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose a resource to download:", reply_markup=reply_markup)

# Function to handle button presses and send files
def button(update: Update, context):
    query = update.callback_query
    resource_name = query.data
    
    # Send the appropriate resource
    file_path = resources.get(resource_name)
    if file_path:
        query.answer()
        context.bot.send_document(chat_id=query.message.chat_id, document=open(file_path, 'rb'))
    else:
        query.answer('Resource not found.')

# Main function to set up the bot
def main():
    # Create an updater object with your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
