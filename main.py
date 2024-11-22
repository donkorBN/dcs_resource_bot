# File: telegram_resource_bot.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import os

# In-memory resource storage (for production, replace with a database)
resources = {
    "pdf": [],
    "ppt": []
}

# Command to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to the Resource Bot!\n"
        "Use /upload to upload resources.\n"
        "Use /resources to access stored resources."
    )

# Command to upload resources
def upload(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Send me the file and specify its type (pdf/ppt) in the caption."
    )

# Handle file uploads
def handle_file_upload(update: Update, context: CallbackContext) -> None:
    if update.message.document:
        file = update.message.document
        caption = update.message.caption.lower() if update.message.caption else None

        if caption in resources:
            resources[caption].append({
                "file_id": file.file_id,
                "file_name": file.file_name
            })
            update.message.reply_text(f"{file.file_name} has been added to {caption} resources!")
        else:
            update.message.reply_text("Invalid type! Use 'pdf' or 'ppt' in the caption.")

# Command to list resources
def resources_command(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("PDFs", callback_data='pdf')],
        [InlineKeyboardButton("PPTs", callback_data='ppt')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select a resource category:", reply_markup=reply_markup)

# Handle resource retrieval
def resource_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    category = query.data
    if resources[category]:
        for resource in resources[category]:
            query.message.reply_document(
                document=resource["file_id"],
                caption=resource["file_name"]
            )
    else:
        query.message.reply_text(f"No {category.upper()} resources available.")

# Main function to run the bot
def main() -> None:
    token = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your bot token
    updater = Updater(token)

    # Command handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("upload", upload))
    updater.dispatcher.add_handler(CommandHandler("resources", resources_command))

    # Message and callback handlers
    updater.dispatcher.add_handler(MessageHandler(Filters.document, handle_file_upload))
    updater.dispatcher.add_handler(CallbackQueryHandler(resource_callback))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
