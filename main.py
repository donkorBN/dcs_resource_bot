import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# In-memory resource storage (for production, replace with a database)
resources = {
    "pdf": [],
    "ppt": []
}

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to the Resource Bot!\n"
        "Use /resources to access stored resources."
    )

# Command to list resources
async def resources_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("PDFs", callback_data='pdf')],
        [InlineKeyboardButton("PPTs", callback_data='ppt')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select a resource category:", reply_markup=reply_markup)

# Handle resource retrieval
async def resource_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    category = query.data
    if resources[category]:
        for resource in resources[category]:
            await query.message.reply_document(
                document=resource["file_id"],
                caption=resource["file_name"]
            )
    else:
        await query.message.reply_text(f"No {category.upper()} resources available.")

# Main function to run the bot
async def main() -> None:
    token = "8069191344:AAFWYeQuXct6ZXcvTcajBFd95XzBJCW6y8o"  # Replace with your bot token

    # Create the application
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("resources", resources_command))

    # Add callback handler
    application.add_handler(CallbackQueryHandler(resource_callback))

    # Run the bot
    print("Bot is running!")
    await application.run_polling()

if __name__ == "__main__":
    main()