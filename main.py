import telebot
from flask import Flask
from threading import Thread

# আপনার তথ্য
API_TOKEN = '8599727244:AAFuffnYlVPaHkbmGmyqBPtZM84OpHG-yL8'
CHANNEL_ID = -1003878856268 # নিশ্চিত হোন এটি সঠিক

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Active!"

# কোনো আইডি চেক ছাড়াই সবার (আপনার) জন্য লিঙ্ক তৈরি করবে
@bot.message_handler(content_types=['photo', 'video', 'document', 'audio'])
def handle_files(message):
    try:
        # সরাসরি চ্যানেলে কপি
        res = bot.copy_message(chat_id=CHANNEL_ID, from_chat_id=message.chat.id, message_id=message.message_id)
        
        # লিঙ্ক তৈরি
        share_link = f"https://t.me/{bot.get_me().username}?start={res.message_id}"
        bot.reply_to(message, f"✅ **Stored!**\n\n🔗 Share Link: `{share_link}`")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 ফাইল পাঠান, লিঙ্ক নিন।")

def run():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
