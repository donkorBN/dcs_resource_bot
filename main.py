import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Your bot token
TOKEN = '8069191344:AAFWYeQuXct6ZXcvTcajBFd95XzBJCW6y8o'

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('resources.db')
    c = conn.cursor()
    
    # Create table for resources
    c.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            file_path TEXT NOT NULL
        )
    ''')
    
    # Insert some sample data
    sample_data = [
        ('Math PPT', 'math_presentation.pptx'),
        ('Physics PDF', 'physics_notes.pdf'),
        ('Chemistry PPT', 'chemistry_intro.pptx')
    ]
    try:
        c.executemany('INSERT INTO resources (name, file_path) VALUES (?, ?)', sample_data)
    except sqlite3.IntegrityError:
        # Ignore if data already exists
        pass
    
    conn.commit()
    conn.close()

# Fetch resources from the SQLite database
def get_resources():
    conn = sqlite3.connect('resources.db')
    c = conn.cursor()
    c.execute("SELECT name FROM resources")
    resources = c.fetchall()
    conn.close()
    return [resource[0] for resource in resources]

# Fetch the file path for a given resource
def get_resource_file_path(name):
    conn = sqlite3.connect('resources.db')
    c = conn.cursor()
    c.execute("SELECT file_path FROM resources WHERE name=?", (name,))
    file_path = c.fetchone()
    conn.close()
    return file_path[0] if file_path else None

# Command to display welcome message
async def welcome(update: Update, context):
    welcome_message = (
        "Hello! Welcome to the Resource Bot.\n\n"
        "You can download various educational resources like PPTs and PDFs here. "
        "Use the /start command to see the list of resources available for download."
    )
    await update.message.reply_text(welcome_message)

# Command to display about information
async def about(update: Update, context):
    about_message = (
        "This is a simple bot that allows you to download educational resources.\n\n"
        "It supports multiple resource categories like Math, Science, and more. "
        "The bot is powered by Python and uses SQLite to manage resources."
    )
    await update.message.reply_text(about_message)

# Start command to display resource buttons
async def start(update: Update, context):
    # Get resources from the database
    resource_names = get_resources()
    keyboard = [[InlineKeyboardButton(resource, callback_data=resource) for resource in resource_names]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Display the buttons
    await update.message.reply_text("Choose a resource to download:", reply_markup=reply_markup)

# Function to handle button presses and send files
async def button(update: Update, context):
    query = update.callback_query
    resource_name = query.data
    
    # Get the file path from the database
    file_path = get_resource_file_path(resource_name)
    if file_path:
        await query.answer()
        with open(file_path, 'rb') as file:
            await context.bot.send_document(chat_id=query.message.chat_id, document=file)
    else:
        await query.answer('Resource not found.')

# Main function to set up the bot
def main():
    # Initialize the database
    init_db()
    
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
