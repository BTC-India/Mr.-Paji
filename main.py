import requests
import logging
import random
import telebot
from configuration.config import API_TOKEN
import utils.logger as logger_save
from telebot.types import InputFile, InputMediaDocument, ChatMemberUpdated

# Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize your custom logger (assuming it writes to a file)
logger_save.init_logger(f"logs/botlog.log")


# Initializing bot with 4 thread workers for handling multiple requests
bot = telebot.TeleBot(API_TOKEN, threaded=True, num_threads=4)


EMOJIS = [
    "😊",
    "🫡",
    "👋",
    "🌞",
    "🌟",
    "🎉",
    "✨",
    "😁",
    "👍",
    "🚀",
    "🤗",
    "🌸",
    "💫",
    "🙌",
    "😃",
    "😎",
    "🌈",
    "🎈",
    "🎊",
    "🦄",
    "💥",
    "🥳",
    "🔥",
    "👏",
    "🎶",
    "🎁",
    "💡",
    "☀️",
    "🍀",
    "🌻",
    "🦋",
    "🌼",
    "🌺",
    "🌀",
    "🌍",
    "🕊️",
    "🌹",
    "🎵",
    "⭐",
    "💖",
    "🥂",
]


# /gm command handler
@bot.message_handler(commands=["gm"])
def gm(message):
    username = message.from_user.username
    chat_id = message.chat.id
    random_emoji = random.choice(EMOJIS)

    # Logging when a user sends a /gm command
    logger.info(f"Received /gm command from {username} (chat_id: {chat_id})")

    # Respond to the user with a good morning message
    bot.send_message(chat_id, f"gm, {username} {random_emoji}")
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
            "bqacaguaaxkdaamszvgtrpjdrfckizjbgp5m93zg6t8aaruraak-ozbxwzftpyid1re2ba",
        )
        logger.info("whitepaper sent successfully")
    except exception as e:
        logger.error(f"failed to send whitepaper: {e}")


# /value : shows realtime value of BTC in INR
@bot.message_handler(commands=["value"])
def value(message):
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
        bot.send_message(chat_id, f"1 BTC = ₹{formatted_value}")
    except exception as e:
        logger.error(f"failed to fetch btc value: {e}")


# welcome
@bot.chat_member_handler()
def on_c(c: ChatMemberUpdated):
    chat_id = c.chat.id
    print("c in on_c:", c)
    if (
        c.new_chat_member
        and c.new_chat_member.status == "member"
        and (
            not c.old_chat_member
            or (c.old_chat_member and c.old_chat_member.status == "kicked")
        )
    ):
        bot.send_message(chat_id, f"gm, new member joined")


# welcome message like in discord
# /social shares social links
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
bot.infinity_polling()
