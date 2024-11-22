# File: telegram_resource_bot.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import os

# In-memory resource storage (for production, replace with a database)
resources = {
    "pdf": [],
    "ppt": []
}

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to the DCS Resource Bot!\n"
        "Use /upload to upload resources.\n"
        "Use /resources to access stored resources."
    )

# Command to upload resources
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Send me the file and specify its type (pdf/ppt) in the caption."
    )

# Handle file uploads
async def handle_file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.document:
        file = update.message.document
        caption = update.message.caption.lower() if update.message.caption else None

        if caption in resources:
            resources[caption].append({
                "file_id": file.file_id,
                "file_name": file.file_name
            })
            await update.message.reply_text(f"{file.file_name} has been added to {caption} resources!")
        else:
            await update.message.reply_text("Invalid type! Use 'pdf' or 'ppt' in the caption.")

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
    application.add_handler(CommandHandler("upload", upload))
    application.add_handler(CommandHandler("resources", resources_command))

    # Add message and callback handlers
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file_upload))
    application.add_handler(CallbackQueryHandler(resource_callback))

    # Start the bot
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
