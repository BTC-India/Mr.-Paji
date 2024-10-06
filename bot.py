import re
import logging
import telebot
import requests
from datetime import datetime
from configuration.config import API_TOKEN, GEMINI_API_KEY
from utils.emojis import EMOJIS
import google.generativeai as genai
from telebot.util import update_types
from telebot.types import (
    ChatMemberUpdated,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import random
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

# Configuring logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Suppress logging from `urllib3` and other external libraries
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Initializing bot with 4 thread workers for handling multiple requests
bot = telebot.TeleBot(API_TOKEN, threaded=True, num_threads=4)

# Chat Id of the group
CHAT_ID = ""

# Initialize gemini models
genai.configure(api_key=GEMINI_API_KEY)
generation_config = genai.GenerationConfig(max_output_tokens=1500)
model = genai.GenerativeModel(model_name='gemini-1.5-flash', generation_config=generation_config, safety_settings={
    "SEXUALLY_EXPLICIT": 'block_none'
})

# Command handlers
# Command - 1: /gm: Say gm
@bot.message_handler(commands=["gm", "start"])
def gm(message: types.Message):
    username = message.from_user.username
    chat_id = message.chat.id
    random_emoji = random.choice(EMOJIS)

    logger.info(
        f"Received /gm or /start command from {username} (chat_id: {chat_id})")
    bot.reply_to(message, f"gm, {username} {random_emoji}")


# Command - 2:  /whitepaper: Shows the Bitcoin whitepaper
@bot.message_handler(commands=["whitepaper"])
def white_paper(message: types.Message):
    chat_id = message.chat.id
    logger.info(f"Sending whitepaper to user: {message.from_user.username}")

    try:
        bot.send_document(
            chat_id,
            "https://bitcoin.org/bitcoin.pdf",
        )
        logger.info("Whitepaper sent successfully")
    except Exception as e:
        logger.error(f"Failed to send whitepaper: {e}")

# Command - 3: /price : shows realtime value of BTC in INR
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

# Command - 4: /social: shares social links
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


# Command - 5: /countdown : countdown till event
@bot.message_handler(commands=["countdown"])
def countdown(message: types.Message):
    username = message.from_user.username
    chat_id = message.chat.id
    logger.info(f"Sending countdown to user: {username} on chat_id: {chat_id}")

    today = datetime.now()
    target_date = datetime(today.year, 12, 16, 10, 0, 0)

    if today >= target_date:
        response = "The event is live now! 🎉🚀 Let's go!"
    else:
        difference = target_date - today
        days_remaining = difference.days
        hours_remaining, remainder = divmod(difference.seconds, 3600)
        minutes_remaining, seconds_remaining = divmod(remainder, 60)

        if days_remaining > 0:
            response = f"Only {days_remaining} day(s) left! 🎉 Get excited! 🚀"
        elif hours_remaining > 0:
            response = f"Just {
                hours_remaining} hour(s) remaining! 🎉 Almost there! 🚀"
        elif minutes_remaining > 0:
            response = f"Only {
                minutes_remaining} minute(s) to go! 🎉 The excitement is building! 🚀"
        else:
            response = f"Only {
                seconds_remaining} second(s) left! 🎉 Get ready! 🚀"

    bot.reply_to(message, response)

# Command - 6 : /satoshi: Send information about satoshi
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


# Command - 7 : /inspire: Send a nice quote
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
        bot.send_message(
            chat_id, "An error occurred while fetching the quote.")
        logger.error(f"Error fetching quote: {e}")

# Command - 8 : /hackathon: Send info about hackathon
@bot.message_handler(commands=["hackathon"])
def hackathon(message):
    username = message.from_user.username
    chat_id = message.chat.id
    logger.info(f"sending hackathon info to user: {
                username} on chat_id: {chat_id}")

    # Crafting a more exciting and detailed response
    reply_message = (
        "🚀 *Get Ready for an Epic 60-Hour Hackathon!* 💻\n\n"
        "More details coming soon! Stay tuned.. ⏳"
    )

    # Sending the reply
    bot.reply_to(message, reply_message, parse_mode="Markdown")

# Command - 9 :/venue: Send the venue
@bot.message_handler(commands=["venue"])
def send_location(message):
    chat_id = message.chat.id
    latitude = 19.133222660801845
    longitude = 72.91503099391358

    # Logging the event
    logger.info(f"sending location to user with chat_id: {chat_id}")

    # Sending the location
    bot.send_location(chat_id, latitude, longitude)

# Command - 10: /akkibhai: Feature akki bhai - Gemini
@bot.message_handler(commands=["akkibhai"])
def akkibhai(message: types.Message):
    username = message.from_user.username
    chat_id = message.chat.id
    logger.info(f"Sending Akki Bhai message to user: {
                username} on chat_id: {chat_id}")

    # Get the respons efrom genai
    response = model.generate_content(
        "Akki bhai is a nice man. Assume he is soon getting married to you, reply him in a funny way like I love u akki bhai. Use emojis, also you are free to send any other message except I love you, but be creative. Message should not exceed 5-10 words. Always tag @Aviraltech")
    reply_message = response.text

    # Send message
    bot.send_message(chat_id, reply_message, parse_mode="Markdown")

# Command - 11: /bitcoinog: Feature bitcoin
@bot.message_handler(commands=["bitcoinog"])
def bitcoin_og(message: types.Message):
    username = message.from_user.username
    chat_id = message.chat.id
    logger.info(f"Sending bitcoin og message to user: {
                username} on chat_id: {chat_id}")

    response = model.generate_content("You need to tell something og about bitcoin not price and other things thing which people don't know generally. Limit your self to 2-4 lines max. Your answer should make people think something completely out of brain. Don't give facts which normal person already know. Also u can make that content as creative as you like. Use emojis also. U can use markdown and make more nice formatting. Try to give unique answer evertime.")
    reply_message = response.text

    bot.send_message(chat_id, reply_message, parse_mode="Markdown")

# Command - 12: '/chatid: Set the chatid
@bot.message_handler(commands=["set_chatid"])
def set_chat_id(message: types.Message):
    global CHAT_ID
    chat_id = message.chat.id
    user_name = message.from_user.username
    if user_name == "scienmanas":
        CHAT_ID = chat_id
        logging.info(f"Chat id set to: {CHAT_ID}")
        bot.reply_to(message, f"Chat Id set successfully :)")
    else:
        logging.info("Not authorized")
        bot.reply_to(message, "Sorry you are not authorized!")


# reply to gm messages
@bot.message_handler(func=lambda msg: True)
def echo_gm(message: types.Message):
    friends = ["mere yaar! 🌞", "buddy! 🌅", "friend! 🌼", "mitr! 🌼"]
    friend_translation = random.choice(friends)
    bot_replied_to = message.reply_to_message is not None

    if re.search(r'\bgm\b', message.text.lower()):
        reply_message = f"Gm, {friend_translation}"
        logging.info("Sending gm")
        bot.reply_to(message, reply_message)
    elif bot_replied_to:
        # Get the text of the message that the user is replying to
        message_from_user = message.text
        original_message_text = message.reply_to_message.text
        prompt = (
            f"Hey! The user just sent you this message: '{
                message_from_user}'. "
            f"Previously, you said: '{original_message_text}'. "
            f"Respond in a funny and friendly manner, using emojis where it feels right! "
            f"If they start asking different questions, simply say: 'I cannot do this.' "
            f"Remember, you are not just any bot; you are Mr. Paji from BTC India! "
            f"Keep your replies short and casual, like you're chatting with a friend."
        )
        print(prompt)
        response = model.generate_content(prompt)

        reply_message = response.text
        bot.reply_to(message, reply_message, parse_mode="Markdown")


# Welcome Message to new joiners
@bot.chat_member_handler()
def on_c(c: ChatMemberUpdated):
    chat_id = c.chat.id
    # Check if a new user has joined the group
    if (
        c.new_chat_member
        and c.new_chat_member.status == "member"
        and (not c.old_chat_member or c.old_chat_member.status in ["left", "kicked"])
    ):
        markup = InlineKeyboardMarkup()
        group = InlineKeyboardButton(
            text="𝕏", url="https://x.com/btcindia_org")
        markup.add(group)
        random_emoji = random.choice(EMOJIS)
        user = c.from_user.username if c.from_user.username else c.from_user.first_name
        caption = (
            f"Welcome @{user} 🌟\n\n"
            "We are building BTC India 🇮🇳. A Bitcoin ₿ focused conf + hackathon.\n"
            "Follow us on our socials so you don't miss any updates!"
        )
        bot.send_photo(
            chat_id,
            "https://i.ibb.co/MfQBsbf/photo-6294318673468440527-y-1.jpg",
            caption=caption,
            reply_markup=markup,
        )

# Scheduler function
def send_btc_hour_reminder():
    reminder_message = (
        f"🚀 Reminder: BTC Hour is happening in 1 hour! 🕰\n\n"
        f"Join us at 9 pm for an exciting discussion "
        f"about the latest in Bitcoin and cryptocurrency.\n\n"
        f"Don't miss out on this opportunity to learn, share, and connect with fellow enthusiasts! 💡🌐"
    )
    try:
        bot.send_message(chat_id=CHAT_ID, text=reminder_message)
        logger.info(f"Sent BTC Hour reminder to group")
    except Exception as e:
        logger.error(f"Failed to send BTC Hour reminder: {e}")


def send_price():
    # log when user requests the value
    logger.info(f"sending btc value")
    try:
        url = "https://api.coinpaprika.com/v1/coins/btc-bitcoin/markets/?quotes=INR"
        response = requests.get(url).json()
        print("response", type(response))
        inr_value = response[0]["quotes"]["INR"]["price"]
        print("INR VALUE:", inr_value)
        formatted_value = (
            f"{inr_value:,.2f}"  # Adds commas and rounds to 2 decimal places
        )
        bot.send_message(chat_id=CHAT_ID, text=f"1 BTC = ₹{formatted_value}")
    except Exception as e:
        logger.error(f"failed to fetch btc value: {e}")


# Load next step handlers from the save file
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

# Function to format datetime in a nice way


def format_time(dt):
    ist = pytz.timezone('Asia/Kolkata')  # Set the timezone to IST
    dt_ist = dt.astimezone(ist)  # Convert the time to IST
    # Format the datetime
    return dt_ist.strftime("%B %d, %Y, at time: %H:%M:%S")


# Main function to start the bot
def start_bot():
    logger.info("Starting the bot :|")
    logging.info("Bot started :)")

    # Initialize the scheduler
    logger.info("Scheduler starting :|")
    scheduler = BackgroundScheduler()
    # Start the scheduler in the background
    reminder_job = scheduler.add_job(
        send_btc_hour_reminder, 'cron', day_of_week='sat', hour=20, minute=0, timezone='Asia/Kolkata')
    price_job = scheduler.add_job(send_price, 'interval', seconds=60*60*6)
    scheduler.start()
    logger.info("Scheduler started :)")
    logger.info(f"First execution of price job: {
                format_time(price_job.next_run_time)}")
    logger.info(f"First execution of reminder job: {
                format_time(reminder_job.next_run_time)}")

    bot.infinity_polling(allowed_updates=update_types)


if __name__ == "__main__":
    start_bot()

