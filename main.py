import logging
import random
import telebot
from configuration.config import API_TOKEN
import utils.logger as logger_save
from telebot.types import InputFile, InputMediaDocument

# Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize your custom logger (assuming it writes to a file)
logger_save.init_logger(f"logs/botlog.log")


# Initializing bot with 4 thread workers for handling multiple requests
bot = telebot.TeleBot(API_TOKEN, threaded=True, num_threads=4)

# Dictionary to store user information
user_dict = {}


# User class to handle user details
class User:
    def __init__(self, name):
        self.name = name
        self.reg_no = None
        self.dob = None
        self.aadhar_no = None


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
    # Log when user requests the whitepaper
    logger.info(f"Sending whitepaper to user with chat_id: {chat_id}")

    try:
        bot.send_document(
            chat_id,
            "BQACAgUAAxkDAAMsZvGtrPJDrFCkiZjBgP5M93Zg6t8AArURAAK-oZBXwZfTpYId1RE2BA",
        )
        logger.info("Whitepaper sent successfully")
    except Exception as e:
        logger.error(f"Failed to send whitepaper: {e}")


# /register command handler
# /social shares social links
# /askme [FAQ] use AI/ML if required
# /venue : venue details
# /countdown : countdown till event
# /speakers : list of speakers
# /workshops : details of workshops
# /hackathon : hackathon details

# Enable saving next step handlers to file "./.handlers-saves/step.save"
bot.enable_save_next_step_handlers(delay=2)

# Load next step handlers from the save file
bot.load_next_step_handlers()

# Logging bot start
logger.info("Bot started and polling...")

# Start polling (infinite loop to keep the bot running)
bot.infinity_polling()
