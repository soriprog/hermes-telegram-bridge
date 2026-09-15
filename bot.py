import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI
import time

# Load environment variables from .env file
load_dotenv()

# Configuration from environment
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("HERMES_API_KEY")
HERMES_BASE_URL = os.getenv("HERMES_BASE_URL", "http://localhost:8000/v1")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "0"))

# Initialize OpenAI-compatible client for Hermes backend
client = OpenAI(
    api_key=API_KEY or "dummy",
    base_url=HERMES_BASE_URL
)

# Setup logging configuration
logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command. Restricts access to authorized user."""
    if ALLOWED_USER_ID and update.effective_user.id != ALLOWED_USER_ID:
        return
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hello! I am your Telegram bot connected to the Hermes AI Agent."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for incoming text messages. Relays user prompt to Hermes LLM."""
    if ALLOWED_USER_ID and update.effective_user.id != ALLOWED_USER_ID:
        return
        
    user_text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(f"Received message from {chat_id}: {user_text}")
    
    # Send typing action to indicate processing
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    start_time = time.time()
    try:
        # Call Hermes API
        response = client.chat.completions.create(
            model="Hermes",
            messages=[
                {"role": "system", "content": "You are Hermes Agent, a helpful AI assistant communicating via Telegram. Respond in Persian (Farsi) unless requested otherwise."},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            timeout=30
        )
        reply = response.choices[0].message.content
        logger.info(f"Responded in {time.time() - start_time:.2f}s")
    except Exception as e:
        logger.error(f"Error calling LLM: {str(e)}")
        reply = f"Error communicating with LLM model: {str(e)}"
        
    await context.bot.send_message(chat_id=chat_id, text=reply)

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN not found in environment.")
        exit(1)
        
    # Build Telegram application
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    logger.info("Bot started successfully.")
    application.run_polling()
