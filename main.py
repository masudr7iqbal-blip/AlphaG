import telebot
from flask import Flask
from threading import Thread

# আপনার তথ্য
API_TOKEN = '8599727244:AAFuffnYlVPaHkbmGmyqBPtZM84OpHG-yL8'
ADMIN_ID = 5716499834 
CHANNEL_ID = -1003878856268 

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

# এটি ফরওয়ার্ড এবং সরাসরি আপলোড করা সব ফাইল রিসিভ করবে
@bot.message_handler(content_types=['video', 'photo', 'document', 'audio'])
def handle_all_files(message):
    # অ্যাডমিন চেক
    if message.from_user.id == ADMIN_ID:
        try:
            # চ্যানেলে কপি করা হচ্ছে
            sent_msg = bot.copy_message(CHANNEL_ID, message.chat.id, message.message_id)
            
            # লিঙ্ক তৈরি
            share_link = f"https://t.me/{bot.get_me().username}?start={sent_msg.message_id}"
            
            bot.reply_to(message, f"✅ **Stored Successfully!**\n\n🔗 লিঙ্ক: `{share_link}`")
        except Exception as e:
            bot.reply_to(message, f"❌ এরর: {str(e)}\nনিশ্চিত করুন বটটি চ্যানেলে অ্যাডমিন আছে।")
    else:
        bot.reply_to(message, "⚠️ আপনি অ্যাডমিন নন।")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 স্বাগতম! যেকোনো ফাইল পাঠান লিঙ্ক তৈরি করতে।")

def run():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
