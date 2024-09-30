import requests
import logging
import time
import schedule
import random
import telebot
from datetime import datetime
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


# Schedule to send Bitcoin price every 6 hours
def schedule_btc_updates():
    # Schedule the task every 6 hours
    schedule.every(6).hours.do(price)

    # Keep the schedule running in an infinite loop
    while True:
        schedule.run_pending()
        time.sleep(1)


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


# /countdown : countdown till event
@bot.message_handler(commands=["countdown"])
def countdown(message):
    username = message.from_user.username
    chat_id = message.chat.id
    logger.info(f"sending countdown to user: {username} on chat_id: {chat_id}")
    today = datetime.today()
    target_date = datetime(today.year, 12, 16)
    days_remaining = (target_date - today).days
    print(f"Days remaining until December 1: {days_remaining}")
    bot.reply_to(message, f"{days_remaining} more to go! 🚀")


# # Command to show the keyboard with an inline button
# @bot.message_handler(commands=["resp"])
# def reply(message):
#     chat_id = message.chat.id
#
#     # Create an Inline Keyboard with a button
#     keyboard = InlineKeyboardMarkup()
#     button = InlineKeyboardButton(text="Received", callback_data="received")
#
#     button2 = InlineKeyboardButton(text="Not Received ", callback_data="nreceived")
#     keyboard.add(button)
#     keyboard.add(button2)
#
#     bot.send_message(
#         chat_id, "Click the button to submit your info", reply_markup=keyboard
#     )
#
#
# @bot.message_handler(content_types=["photo"])
# def handle_photo(message):
#     # chat_id = message.chat.id
#     chat_id = -1002340040662
#     photo = message.photo[-1].file_id  # Get the highest resolution photo
#     keyboard = InlineKeyboardMarkup()
#     button = InlineKeyboardButton(text="Received", callback_data="received")
#
#     button2 = InlineKeyboardButton(text="Not Received ", callback_data="nreceived")
#     keyboard.add(button)
#     keyboard.add(button2)
#
#     # Log info
#     bot.send_message(chat_id, "Photo received. Sending it back to you...")
#
#     # Send the photo back to the user
#     bot.send_photo(
#         chat_id, photo, caption="Here is the photo you sent!", reply_markup=keyboard
#     )
#
#
# # Handle the button click with callback_data
# @bot.callback_query_handler(func=lambda call: True)
# def handle_callback_query(call):
#     user_chat_id = 990333293
#     if call.data == "received":
#         bot.send_message(user_chat_id, "Received")
#     if call.data == "nreceived":
#         bot.send_message(user_chat_id, "Not Received")
#         # Here you can set up further handling to receive user input
#


# /satoshi command handler
@bot.message_handler(commands=["satoshi"])
def satoshi_info(message):
    chat_id = message.chat.id

    # Satoshi Nakamoto's history and conspiracy theories
    satoshi_message = (
        "👤 *Satoshi Nakamoto* is the mysterious figure or group who created Bitcoin in 2008 and authored the Bitcoin whitepaper. "
        "Satoshi introduced Bitcoin as a decentralized, peer-to-peer electronic cash system, allowing online payments to be sent directly without the need for a trusted third party.\n\n"
        "🔍 After releasing the whitepaper, Nakamoto continued to contribute to Bitcoin development but disappeared from public view in 2011, leaving the community to carry on the project. "
        "Satoshi's identity remains unknown, leading to many conspiracy theories:\n\n"
        "1️⃣ *Satoshi was a government agency or group* – Some believe that a state or a group of researchers developed Bitcoin for financial or political reasons.\n"
        "2️⃣ *Satoshi is an individual genius* – Some think Satoshi is a lone cryptography expert with deep knowledge of economics and technology.\n"
        "3️⃣ *Satoshi faked his disappearance* – A common theory is that Satoshi staged his disappearance to avoid legal, financial, or social implications.\n"
        "4️⃣ *Satoshi is dead* – Some believe Satoshi might have passed away, which explains the lack of communication since 2011.\n\n"
        "🌐 Despite the mystery, Satoshi's legacy continues, with Bitcoin growing to be a major force in global finance. Whoever they are, their work has changed the world forever!"
    )

    markup = InlineKeyboardMarkup()
    group = InlineKeyboardButton(text="₿", url="https://bitcoin.org/en/")

    # add the button to markup
    markup.add(group)

    # Send the message
    bot.send_message(
        chat_id, satoshi_message, parse_mode="Markdown", reply_markup=markup
    )


# /inspire command handler
@bot.message_handler(commands=["inspire"])
def inspire_quote(message):
    chat_id = message.chat.id

    # Fetch a random quote from ZenQuotes API
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            quote_data = response.json()[
                0
            ]  # The API returns a list with a single dictionary

            # Extract the quote and author
            quote = quote_data["q"]
            author = quote_data["a"]

            # Format the message
            inspire_message = f'"{quote}"\n\n— *{author}*'
            bot.send_message(chat_id, inspire_message, parse_mode="Markdown")
        else:
            bot.send_message(
                chat_id,
                "Sorry, couldn't fetch the quote at this time. Please try again later.",
            )
    except Exception as e:
        bot.send_message(chat_id, "An error occurred while fetching the quote.")
        logger.error(f"Error fetching quote: {e}")


# /hackathon command handler
@bot.message_handler(commands=["hackathon"])
def hackathon(message):
    username = message.from_user.username
    chat_id = message.chat.id
    logger.info(f"sending hackathon info to user: {username} on chat_id: {chat_id}")

    # Crafting a more exciting and detailed response
    reply_message = (
        "🚀 *Get Ready for an Epic 60-Hour Hackathon!* 💻\n\n"
        "More details coming soon! Stay tuned.. ⏳"
    )

    # Sending the reply
    bot.reply_to(message, reply_message, parse_mode="Markdown")


# /venue command handler
@bot.message_handler(commands=["venue"])
def send_location(message):
    chat_id = message.chat.id
    latitude = 19.133222660801845
    longitude = 72.91503099391358

    # Logging the event
    logger.info(f"sending location to user with chat_id: {chat_id}")

    # Sending the location
    bot.send_location(chat_id, latitude, longitude)


# reply to gm messages
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    # List of 'friend' in different languages
    friends = [
        "amigo",
        "freund",
        "ami",
        "kaibigan",
        "친구",
        "友達",
        "приятель",
        "amico",
        "dost",
        "phít",
    ]
    if message.text.lower() == "gm":
        friend_translation = random.choice(friends)
        reply_message = f"{message.text}, {friend_translation}!"
        bot.reply_to(message, reply_message)


# welcome
# @bot.chat_member_handler()
# def on_c(c: ChatMemberUpdated):
#     print("c in on_c:", c)
#     chat_id = c.chat.id
#     if (
#         c.new_chat_member
#         and c.new_chat_member.status == "member"
#         and (
#             not c.old_chat_member
#             or (c.old_chat_member and c.old_chat_member.status == "kicked")
#         )
#     ):
#         bot.send_message(chat_id, f"gm, {c.from_user.first_name}")
#

# /askme [FAQ] use AI/ML if required
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
# bot.infinity_polling(allowed_updates=update_types) # for welcome messages
bot.infinity_polling()
