import telebot  # Corrected 'import'
from telebot import types
import time
import threading
import json
import os

# 1. Bot Token and Admin ID
TOKEN = '8736077948:AAF8BpxUzmPUhWR4IJLFRtxJn_1ua--0fZ8'
ADMIN_ID = 8692510107
bot = telebot.TeleBot(TOKEN)

# 2. Media and Links
THUMBNAIL_URL = 'https://i.ibb.co/ZRRZJ6J4/IMG-20260510-WA0079.jpg' 
QR_URL = 'https://i.ibb.co/3Ydx3V1Y/IMG-20260511-171128-380.jpg'
DOWNLOAD_LINK = "https://t.me/dirp_client"

# --- 3. Database Logic ---
DB_FILE = "live_stats.json"

def load_stats():
    if not os.path.exists(DB_FILE):
        return {"users": [], "total_cash": 0, "sales_count": {}}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {"users": [], "total_cash": 0, "sales_count": {}}

def save_stats(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

active_timers = {}

# 4. Product Database
PRODUCT_PLANS = {
    "DRIP_APK": {"name": "DRIP CLIENT APK", "plans": [("1 Day", 90), ("3 Day", 220), ("7 Day", 340), ("15 Day", 600), ("30 Day", 800)]},
    "DRIP_PC": {"name": "DRIP CLIENT PC", "plans": [("1 Day", 150), ("7 Day", 500), ("30 Day", 1200)]},
    "DRIP_ROOT": {"name": "DRIP CLIENT ROOT", "plans": [("1 Day", 100), ("7 Day", 400), ("30 Day", 900)]},
    "FLUORITE": {"name": "FLUORITE iOS", "plans": [("1 Day", 450), ("7 Day", 1400), ("31 Day", 2200)]},
    "HAXX_PRO": {"name": "HAXX-CKER PRO", "plans": [("10 Day", 749), ("20 Day", 1240), ("30 Day", 1600)]},
    "HAXX_NON": {"name": "HAXX-CKER NONROOT", "plans": [("10 Day", 550), ("20 Day", 1000), ("30 Day", 1300)]},
    "HG_CHEAT": {"name": "HG CHEATS APK", "plans": [("1 Day", 110), ("7 Day", 230), ("10 Day", 400), ("30 Day", 700)]},
    "REAPER_P": {"name": "REAPER X PRO", "plans": [("10 Day", 445), ("20 Day", 950), ("30 Day", 1400)]},
    "REAPER_N": {"name": "REAPERX NON ROOT", "plans": [("10 Day", 420), ("20 Day", 900), ("30 Day", 1200)]},
    "LKTEAM": {"name": "LKTEAM ROOT + PC", "plans": [("1 Day", 110), ("5 Day", 230), ("10 Day", 400), ("30 Day", 900)]},
    "PATO_ORG": {"name": "PATOTEAM APK+ROOT", "plans": [("1 Day", 200), ("3 Day", 270), ("7 Day", 400), ("15 Day", 700), ("30 Day", 1300)]},
    "PATO_BLU": {"name": "PATOTEAM BLUE APK+ROOT", "plans": [("3 Day", 300), ("7 Day", 500), ("15 Day", 650), ("30 Day", 1200)]},
    "TERMINAL": {"name": "TERMINAL x999 PC", "plans": [("30 Day", 100)]},
    "PRIME": {"name": "PRIME HOOK APK", "plans": [("1 Day", 100), ("3 Day", 230), ("7 Day", 400)]},
    "BR_ROOT": {"name": "BR MODS ROOT", "plans": [("1 Day", 110), ("7 Day", 350), ("15 Day", 550), ("30 Day", 800)]},
    "STRICKS": {"name": "STRICKS BR MODS", "plans": [("1 Day", 90), ("5 Day", 200), ("10 Day", 150), ("15 Day", 400), ("30 Day", 150)]},
    "SPOTIFY": {"name": "SPOTIFY ROOT", "plans": [("7 Day", 300), ("15 Day", 400), ("30 Day", 600), ("60 Day", 900)]}
}

# --- 5. ADMIN COMMANDS ---
@bot.message_handler(commands=['kodom'])
def show_live_status(message):
    if message.chat.id != ADMIN_ID: return
    
    data = load_stats()
    status_msg = "📊 **DRIP STORE LIVE REPORT**\n"
    status_msg += "━━━━━━━━━━━━━━━━━━━━━\n\n"
    status_msg += f"👥 **Total Active Users:** {len(data['users'])}\n"
    status_msg += f"💰 **Total In-Bank:** ₹{data['total_cash']}\n\n"
    status_msg += "📦 **Sales Details:**\n"
    
    if not data['sales_count']:
        status_msg += "├ No products sold yet.\n"
    else:
        for p_id, count in data['sales_count'].items():
            p_name = PRODUCT_PLANS.get(p_id, {}).get('name', p_id)
            status_msg += f"├ {p_name}: {count} Sold\n"
            
    status_msg += "\n━━━━━━━━━━━━━━━━━━━━━\n"
    status_msg += "✅ *Live tracking enabled.*"
    bot.send_message(ADMIN_ID, status_msg, parse_mode="Markdown")

# --- 6. USER HANDLERS ---

@bot.message_handler(commands=['help'])
def send_help(message):
    uid = message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("💬 WHATSAPP SUPPORT 1", url="https://wa.me/917896222050")
    btn2 = types.InlineKeyboardButton("💬 WHATSAPP SUPPORT 2", url="https://wa.me/917002386889")
    btn3 = types.InlineKeyboardButton("💬 WHATSAPP SUPPORT 3", url="https://wa.me/916901838086")
    markup.add(btn1, btn2, btn3)
    
    help_text = (
        "🆘 **HELP & CUSTOMER SUPPORT**\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "Facing issues with delivery or have a question?\n\n"
        "💡 **Don't Worry!** Click any button below to chat with me directly on WhatsApp.\n\n"
        "📌 **Required Information:**\n"
        "├ Keep Payment Screenshot ready\n"
        "└ Your User ID: `{uid}`\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "✨ **We are trying to solve your problem ASAP!**"
    ).format(uid=uid)
    bot.send_message(uid, help_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    uid = message.chat.id
    
    data = load_stats()
    if uid not in data['users']:
        data['users'].append(uid)
        save_stats(data)

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🛒 BROWSE PRODUCT STORE", callback_data="product_store"),
        types.InlineKeyboardButton("📥 DOWNLOAD ALL PANELS", url=DOWNLOAD_LINK),
        types.InlineKeyboardButton("🆘 GET HELP / SUPPORT", callback_data="get_help")
    )
    
    welcome_text = (
        f"👋 **Hello {message.from_user.first_name}!**\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "✨ **Welcome to DRIP KEY STORE** ✨\n\n"
        "🚀 **Why Choose Us?**\n"
        "├ 🔥 Premium Gaming Panels at Lowest Price\n"
        "├ 🛡️ 100% Secure & Anti-Ban Scripts\n"
        "├ ⚡ Instant Key Delivery System\n"
        "└ 🛠️ Full Setup Support & Guidelines\n"
        "━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.send_photo(uid, THUMBNAIL_URL, caption=welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    uid = call.message.chat.id
    mid = call.message.message_id

    if call.data == "product_store":
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(f"👉 {data['name']}", callback_data=f"buy:{key}") for key, data in PRODUCT_PLANS.items()]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("⬅️ BACK TO MAIN MENU", callback_data="back_home"))
        bot.edit_message_caption("🛒 **OFFICIAL PREMIUM STORE**\n\n*Please select a product to see plans:*", uid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "get_help":
        bot.delete_message(uid, mid)
        send_help(call.message)

    elif call.data.startswith("buy:"):
        p_key = call.data.split(":")[1]
        product = PRODUCT_PLANS[p_key]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, (p_name, price) in enumerate(product['plans']):
            markup.add(types.InlineKeyboardButton(f"⏱️ {p_name} - ₹{price}", callback_data=f"pay:{p_key}:{i}"))
        markup.add(types.InlineKeyboardButton("⬅️ BACK", callback_data="product_store"))
        bot.edit_message_caption(f"🎥 **PRODUCT: {product['name']}**\n\n*Choose your preferred duration below:*", uid, mid, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("pay:"):
        _, p_key, p_idx = call.data.split(":")
        plan_name, price = PRODUCT_PLANS[p_key]['plans'][int(p_idx)]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ I HAVE PAID - VERIFY", callback_data=f"utr:{p_key}:{p_idx}"))
        markup.add(types.InlineKeyboardButton("❌ CANCEL ORDER", callback_data="back_home"))
        
        bot.delete_message(uid, mid)
        qr_cap = (
            f"💳 **SECURE PAYMENT GATEWAY**\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"📦 **Product:** {PRODUCT_PLANS[p_key]['name']}\n"
            f"⏱️ **Duration:** {plan_name}\n"
            f"💰 **Total Price:** ₹{price}\n\n"
            f"📢 *Instructions:* Scan the QR code, complete the payment, and click the verify button below."
        )
        bot.send_photo(uid, QR_URL, caption=qr_cap, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("utr:"):
        _, p_key, p_idx = call.data.split(":")
        msg = bot.send_message(uid, "📝 **Please enter your 12-digit Transaction UTR ID to verify:**")
        bot.register_next_step_handler(msg, lambda m: process_verification(m, p_key, p_idx))

    elif call.data == "back_home":
        bot.delete_message(uid, mid)
        send_welcome(call.message)

    elif call.data.startswith("adm_ok:"):
        parts = call.data.split(":")
        target_id = parts[1]
        p_key = parts[2]
        price = int(parts[3]) if len(parts) > 3 else 0
        
        prompt = bot.send_message(ADMIN_ID, f"⌨️ **Type the KEY for {PRODUCT_PLANS[p_key]['name']}:**")
        bot.delete_message(ADMIN_ID, mid)
        bot.register_next_step_handler(prompt, lambda m: deliver_product(m, target_id, p_key, price))

    elif call.data.startswith("adm_no:"):
        target_id = int(call.data.split(":")[1])
        if target_id in active_timers:
            try: bot.delete_message(target_id, active_timers[target_id])
            except: pass
            del active_timers[target_id]
        bot.send_message(target_id, "❌ **Payment Rejected!**\nAdmin has rejected your request.")
        bot.edit_message_text("❌ **Payment Rejected!**", ADMIN_ID, mid)

def process_verification(message, p_key, p_idx):
    uid = message.chat.id
    utr = message.text
    product = PRODUCT_PLANS[p_key]
    plan_name, price = product['plans'][int(p_idx)]
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ ACCEPT", callback_data=f"adm_ok:{uid}:{p_key}:{price}"),
        types.InlineKeyboardButton("❌ REJECT", callback_data=f"adm_no:{uid}")
    )
    admin_text = (
        f"🔔 **NEW ORDER ALERT!**\n"
        f"👤 User: {message.from_user.first_name} (`{uid}`)\n"
        f"📦 {product['name']}\n"
        f"💰 ₹{price}\n"
        f"📝 UTR: `{utr}`"
    )
    bot.send_message(ADMIN_ID, admin_text, reply_markup=markup)
    
    timer_msg = bot.send_message(uid, "⏳ **Verifying... Please wait.**")
    active_timers[uid] = timer_msg.message_id
    threading.Thread(target=run_countdown, args=(uid, timer_msg.message_id)).start()

def run_countdown(uid, mid):
    for i in range(59, -1, -1):
        if uid not in active_timers: return
        try:
            bot.edit_message_text(f"⏳ **Verifying... ({i}s)**", uid, mid)
            time.sleep(1)
        except: break

def deliver_product(message, target_id, p_key, price):
    key_data = message.text
    target_id = int(target_id)
    
    data = load_stats()
    data['total_cash'] += price
    data['sales_count'][p_key] = data['sales_count'].get(p_key, 0) + 1
    save_stats(data)

    if target_id in active_timers:
        try: bot.delete_message(target_id, active_timers[target_id])
        except: pass
        del active_timers[target_id]

    delivery_text = (
        f"🎁 **ORDER COMPLETED!**\n"
        f"📦 **Product:** {PRODUCT_PLANS[p_key]['name']}\n"
        f"🔑 **Key:** `{key_data}`"
    )
    bot.send_message(target_id, delivery_text, parse_mode="Markdown")
    bot.send_message(ADMIN_ID, f"✅ Delivered! 💰 Added ₹{price}")

print("Bot is running...")
bot.infinity_polling()
