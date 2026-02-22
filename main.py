import telebot
import time
import threading
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- আপনার সেটিংস ---
API_TOKEN = '8599727244:AAFuffnYlVPaHkbmGmyqBPtZM84OpHG-yL8'
ADMIN_ID = 5716499834 
CHANNEL_ID = -1003878856268 
MUST_JOIN_CHANNEL = "https://t.me/+LFEmWRfqWmhjMmZl"

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Alpha Drive is Live!"

# --- ফাইল অটো-ডিলিট ফাংশন ---
def delete_msg(chat_id, message_id):
    time.sleep(600) # ১০ মিনিট = ৬০০ সেকেন্ড
    try:
        bot.delete_message(chat_id, message_id)
        bot.send_message(chat_id, "⚠️ **নিরাপত্তার কারণে ফাইলটি ১০ মিনিট পর মুছে ফেলা হয়েছে।**")
    except:
        pass

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    markup = InlineKeyboardMarkup()
    btn_join = InlineKeyboardButton("📢 Join Channel", url=MUST_JOIN_CHANNEL)
    markup.add(btn_join)

    if len(args) > 1:
        file_id = args[1]
        btn_get = InlineKeyboardButton("🔓 Get File", callback_data=f"get_{file_id}")
        markup.add(btn_get)
        text = "🚀 **Alpha Drive Premium**\n\n📥 *ফাইলটি পেতে নিচের বাটনে ক্লিক করুন:*"
    else:
        text = "👋 **Welcome!**\nযেকোনো ফাইল স্টোর করতে আমাকে এখানে পাঠান।"

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('get_'))
def get_file(call):
    file_msg_id = call.data.split('_')[1]
    bot.edit_message_text("⌛ Processing...", call.message.chat.id, call.message.message_id)
    time.sleep(2)
    
    try:
        sent_msg = bot.copy_message(call.message.chat.id, CHANNEL_ID, int(file_msg_id))
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "✅ **ফাইলটি ১০ মিনিট পর অটোমেটিক ডিলিট হয়ে যাবে।**")
        
        # ডিলিট টাইমার চালু
        threading.Thread(target=delete_msg, args=(call.message.chat.id, sent_msg.message_id)).start()
    except:
        bot.send_message(call.message.chat.id, "❌ ফাইলটি পাওয়া যায়নি।")

def run():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()
