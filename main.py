import requests
import logging
import random
import telebot
from configuration.config import API_TOKEN
from utils.emojis import EMOJIS
import utils.logger as logger_save
from telebot.util import update_types
from telebot.types import (
    InputFile,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ChatMemberUpdated,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


# Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize your custom logger (assuming it writes to a file)
logger_save.init_logger(f"logs/botlog.log")


# Initializing bot with 4 thread workers for handling multiple requests
bot = telebot.TeleBot(API_TOKEN, threaded=True, num_threads=4)


# /gm command handler
@bot.message_handler(commands=["gm", "start"])
def gm(message):
    username = message.from_user.username
    chat_id = message.chat.id
    random_emoji = random.choice(EMOJIS)

    # Logging when a user sends a /gm command
    logger.info(f"Received /gm command from {username} (chat_id: {chat_id})")

    # Respond to the user with a good morning message
    # bot.send_message(chat_id, f"gm, {username} {random_emoji}")
    bot.reply_to(message, f"gm, {username} {random_emoji}")
    return


# /whitepaper command handler
@bot.message_handler(commands=["whitepaper"])
def white_paper(message):
    chat_id = message.chat.id
    # log when user requests the whitepaper
    logger.info(f"sending whitepaper to user with chat_id: {chat_id}")

    try:
        bot.send_document(
            chat_id,
            "BQACAgUAAyEGAASMAc6ZAAM3ZvKSFE1Mj4ZJ3MksBalRTIF15s8AAtsTAAI0JphXM7E_jzcS-X42BA",
        )
        logger.info("whitepaper sent successfully")
    except Exception as e:  # Use 'Exception' to catch errors
        logger.error(f"failed to send whitepaper: {e}")


# /price : shows realtime value of BTC in INR
@bot.message_handler(commands=["price"])
def price(message):
    chat_id = message.chat.id
    # log when user requests the value
    logger.info(f"sending btc value to user with chat_id: {chat_id}")
    try:
        url = "https://api.coinpaprika.com/v1/coins/btc-bitcoin/markets/?quotes=INR"
        response = requests.get(url).json()
        print("response", type(response))
        inr_value = response[0]["quotes"]["INR"]["price"]
        print("INR VALUE:", inr_value)
        formatted_value = (
            f"{inr_value:,.2f}"  # Adds commas and rounds to 2 decimal places
        )
        bot.reply_to(message, f"1 BTC = ₹{formatted_value}")
    except Exception as e:
        logger.error(f"failed to fetch btc value: {e}")


# /social shares social links
@bot.message_handler(commands=["social"])
def social(message):
    username = message.from_user.username
    chat_id = message.chat.id
    logger.info(f"sending social link user: {username} on chat_id: {chat_id}")

    markup = InlineKeyboardMarkup()
    group = InlineKeyboardButton(text="𝕏", url="https://x.com/btcindia_org")

    # add the button to markup
    markup.add(group)

    # display this markup:
    bot.reply_to(
        message,
        "Follow us on our socials so you don't miss any updates!",
        reply_markup=markup,
    )


# welcome
@bot.chat_member_handler()
def on_c(c: ChatMemberUpdated):
    print("c in on_c:", c)
    chat_id = c.chat.id
    bot.send_message(chat_id, f"gm, {c.from_user.first_name}")


# /askme [FAQ] use AI/ML if required
# /venue : venue details
# /countdown : countdown till event
# /speakers : list of speakers
# /workshops : details of workshops
# /hackathon : hackathon details
# /inspire: share a inspire quote use external api

# Enable saving next step handlers to file "./.handlers-saves/step.save"
bot.enable_save_next_step_handlers(delay=2)

# Load next step handlers from the save file
bot.load_next_step_handlers()

# Logging bot start
logger.info("Bot started and polling...")

# Start polling (infinite loop to keep the bot running)
bot.infinity_polling(allowed_updates=update_types)
