from pyrogram import *
from info import *
import asyncio
from Script import script
from .database import *
import re
import time  # <-- Added for broadcast sleep
from pyrogram.errors import FloodWait
from pyrogram.types import *

@Client.on_message(filters.command("start") & filters.private)
async def strtCap(bot, message):
    user_id = int(message.from_user.id)
    if await is_user_banned(user_id):  # <-- এই লাইনটি যোগ করুন
        return                         # <-- এই লাইনটি যোগ করুন
    await insert(user_id)
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕️ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ➕️", url=f"https://t.me/Auto_Caption_Prime_Bot?startchannel=true")
            ],[
                InlineKeyboardButton("Hᴇʟᴘ", callback_data="help"),
                InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="about")
            ],[
                InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/PrimeXBots"),
                InlineKeyboardButton("💬 ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url=r"https://t.me/Prime_Support_Group")
            ],[                
                InlineKeyboardButton("☆💫 𝗖𝗥𝗘𝗔𝗧𝗢𝗥 💫☆", url=r"https://t.me/Prime_Nayem")
        ]]
    )
    await message.reply_photo(
        photo=PRIME_PIC,
        caption=f"<b>Hᴇʟʟᴏ {message.from_user.mention}\n\nɪ ᴀᴍ ᴀᴜᴛᴏ ᴄᴀᴘᴛɪᴏɴ ʙᴏᴛ ᴡɪᴛʜ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ.\n\nFᴏʀ ᴍᴏʀᴇ ɪɴғᴏ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ.\n\n <blockquote>⚙️ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ ➠ <a href='https://t.me/PrimeXBots'>ᴘʀɪᴍᴇXʙᴏᴛs</a></blockquote></b>",
        reply_markup=keyboard
    )

@Client.on_message(filters.private & filters.user(ADMIN)  & filters.command(["total_users"]))
async def all_db_users_here(client,message):
    silicon = await message.reply_text("Please Wait....")
    primexbots = await total_user()
    await silicon.edit(f"Tᴏᴛᴀʟ Usᴇʀ :- `{primexbots}`")

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
    if message.reply_to_message:
        status = await message.reply("Broadcast processing...")
        users = await getid()
        tot = await total_user()
        success = failed = deactivated = blocked = 0

        for user in users:
            try:
                await message.reply_to_message.copy(user['_id'])
                success += 1
            except errors.InputUserDeactivated:
                deactivated += 1
                await delete({"_id": user['_id']})
            except errors.UserIsBlocked:
                blocked += 1
                await delete({"_id": user['_id']})
            except FloodWait as e:
                await asyncio.sleep(e.x)  # <-- Fixed variable name from t.x to e.x
                continue
            except Exception:
                failed += 1
                await delete({"_id": user['_id']})

        await status.edit(
            f"<u>Broadcast completed</u>\n\n• Total users: {tot}\n• Successful: {success}\n• Blocked: {blocked}\n• Deactivated: {deactivated}\n• Failed: {failed}"
        )

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command("restart"))
async def restart_bot(b, m):
    msg = await b.send_message("Restarting bot...", chat_id=m.chat.id)
    await asyncio.sleep(3)
    await msg.edit("Bot restarted successfully.")
    os.execl(sys.executable, sys.executable, *sys.argv)

#====================== BAN/UNBAN FUNCTIONALITY START ======================#

# Ban a user
@Client.on_message(filters.command("ban_user") & filters.user(ADMIN))
async def ban_a_user(client, message):
    if len(message.command) == 1 and not message.reply_to_message:
        return await message.reply_text(
            "ℹ️ **Usage:**\n- Reply to a user's message with `/ban_user`.\n- Use `/ban_user [user_id]`."
        )

    try:
        user_id = int(message.command[1]) if len(message.command) > 1 else message.reply_to_message.from_user.id
        if await is_user_banned(user_id):
            return await message.reply_text("This user is already banned.")
            
        user = await client.get_users(user_id)
        await add_user_ban(user.id)
        await message.reply_text(f"✅ **Successfully Banned!**\n\n**User:** {user.mention}\n**ID:** `{user.id}`")

    except ValueError:
        await message.reply_text("⚠️ Please provide a valid User ID.")
    except Exception as e:
        await message.reply_text(f"❌ Could not find the user or another error occurred: `{e}`")

# Unban a user
@Client.on_message(filters.command("unban_user") & filters.user(ADMIN))
async def unban_a_user(client, message):
    if len(message.command) == 1 and not message.reply_to_message:
        return await message.reply_text(
            "ℹ️ **Usage:**\n- Reply to a user's message with `/unban_user`.\n- Use `/unban_user [user_id]`."
        )

    try:
        user_id = int(message.command[1]) if len(message.command) > 1 else message.reply_to_message.from_user.id
        if not await is_user_banned(user_id):
            return await message.reply_text("This user is not banned.")

        user = await client.get_users(user_id)
        await rm_user_ban(user.id)
        await message.reply_text(f"✅ **Successfully Unbanned!**\n\n**User:** {user.mention}\n**ID:** `{user.id}`")

    except ValueError:
        await message.reply_text("⚠️ Please provide a valid User ID.")
    except Exception as e:
        await message.reply_text(f"❌ Could not find the user or another error occurred: `{e}`")

# Ban a channel
@Client.on_message(filters.command("ban_channel") & filters.user(ADMIN))
async def ban_a_channel(client, message):
    if len(message.command) < 2:
        return await message.reply_text("ℹ️ **Usage:** `/ban_channel [channel_id]`")
    
    try:
        channel_id = int(message.command[1])
        if await is_chnl_banned(channel_id):
            return await message.reply_text("This channel is already banned.")

        chat = await client.get_chat(channel_id)
        await add_chnl_ban(chat.id)
        await message.reply_text(f"✅ **Channel Successfully Banned!**\n\n**Channel:** {chat.title}\n**ID:** `{chat.id}`")

    except ValueError:
        await message.reply_text("⚠️ Please provide a valid Channel ID. It must start with `-100`.")
    except Exception as e:
        await message.reply_text(f"❌ Could not find the channel or another error occurred: `{e}`")

# Unban a channel
@Client.on_message(filters.command("unban_channel") & filters.user(ADMIN))
async def unban_a_channel(client, message):
    if len(message.command) < 2:
        return await message.reply_text("ℹ️ **Usage:** `/unban_channel [channel_id]`")
        
    try:
        channel_id = int(message.command[1])
        if not await is_chnl_banned(channel_id):
            return await message.reply_text("This channel is not banned.")

        chat = await client.get_chat(channel_id)
        await rm_chnl_ban(chat.id)
        await message.reply_text(f"✅ **Channel Successfully Unbanned!**\n\n**Channel:** {chat.title}\n**ID:** `{chat.id}`")

    except ValueError:
        await message.reply_text("⚠️ Please provide a valid Channel ID. It must start with `-100`.")
    except Exception as e:
        await message.reply_text(f"❌ Could not find the channel or another error occurred: `{e}`")

#====================== BAN/UNBAN FUNCTIONALITY END ======================#
    
@Client.on_message(filters.command("set_cap") & filters.channel)
async def setCap(bot, message):
    if len(message.command) < 2:
        return await message.reply(
            "Usᴀɢᴇ: **/set_cap 𝑌𝑜𝑢𝑟 𝑐𝑎𝑝𝑡𝑖𝑜𝑛 𝑈𝑠𝑒 <code>{file_name}</code> 𝑇𝑜 𝑠ℎ𝑜𝑤 𝑦𝑜𝑢𝑟 𝐹𝑖𝑙𝑒 𝑁𝑎𝑚𝑒.\n\n𝑈𝑠𝑒<code>{file_size}</code> 𝑇𝑜 𝑠ℎ𝑜𝑤 𝑦𝑜𝑢𝑟 𝐹𝑖𝑙𝑒 𝑆𝑖𝑧𝑒/n/n✓ 𝑀𝑎𝑦 𝐵𝑒 𝑁𝑜𝑤 𝑌𝑜𝑢 𝑎𝑟𝑒 𝑐𝑙𝑒𝑎𝑟💫**"
        )
    chnl_id = message.chat.id
    caption = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    )
    chkData = await chnl_ids.find_one({"chnl_id": chnl_id})
    if chkData:
        await updateCap(chnl_id, caption)
        return await message.reply(f"Your New Caption: {caption}")
    else:
        await addCap(chnl_id, caption)
        return await message.reply(f"Yᴏᴜʀ Nᴇᴡ Cᴀᴘᴛɪᴏɴ Is: {caption}")

@Client.on_message(filters.command("del_cap") & filters.channel)
async def delCap(_, msg):
    chnl_id = msg.chat.id
    try:
        await chnl_ids.delete_one({"chnl_id": chnl_id})
        return await msg.reply("<b><i>✓ Sᴜᴄᴄᴇssғᴜʟʟʏ... Dᴇʟᴇᴛᴇᴅ Yᴏᴜʀ Cᴀᴘᴛɪᴏɴ Nᴏᴡ I ᴀᴍ Usɪɴɢ Mʏ Dᴇғᴀᴜʟᴛ Cᴀᴘᴛɪᴏɴ </i></b>")
    except Exception as e:
        e_val = await msg.replay(f"ERR I GOT: {e}")
        await asyncio.sleep(5)
        await e_val.delete()
        return

def extract_language(default_caption):
    language_map = {
        "hindi": "Hindi", "hi": "Hindi", "hin": "Hindi",
        "english": "English", "en": "English",
        "tamil": "Tamil", "ta": "Tamil",
        "telugu": "Telugu", "te": "Telugu",
        "malayalam": "Malayalam", "ml": "Malayalam",
        "kannada": "Kannada", "kn": "Kannada",
        # Bengali & Bangla আলাদা + ba এড
        "bengali": "Bengali", "bn": "Bengali",
        "bangla": "Bangla", "ba": "Bangla",
        "punjabi": "Punjabi", "pa": "Punjabi",
        "marathi": "Marathi", "mr": "Marathi",
        "gujarati": "Gujarati", "gu": "Gujarati",
        "bhojpuri": "Bhojpuri",
        "urdu": "Urdu", "ur": "Urdu",
        "korean": "Korean", "ko": "Korean",
        "japanese": "Japanese", "ja": "Japanese", "jp": "Japanese",
        "chinese": "Chinese", "zh": "Chinese", "cn": "Chinese",
        "spanish": "Spanish", "es": "Spanish",
        "french": "French", "fr": "French",
        "german": "German", "de": "German",
        "russian": "Russian", "ru": "Russian",
        "arabic": "Arabic", "ar": "Arabic",
        "turkish": "Turkish", "tr": "Turkish",
        "thai": "Thai", "th": "Thai",
        "sinhala": "Sinhala", "si": "Sinhala",
        "oriya": "Oriya", "odia": "Oriya", "or": "Oriya",
        "assamese": "Assamese", "as": "Assamese",
        "nepali": "Nepali", "ne": "Nepali",
        "filipino": "Filipino", "tagalog": "Filipino", "fil": "Filipino", "tl": "Filipino",
        "vietnamese": "Vietnamese", "vi": "Vietnamese",
        "portuguese": "Portuguese", "pt": "Portuguese",
        "italian": "Italian", "it": "Italian",
        "dutch": "Dutch", "nl": "Dutch",
        "swedish": "Swedish", "sv": "Swedish",
        "norwegian": "Norwegian", "no": "Norwegian",
        "polish": "Polish", "pl": "Polish",
        "czech": "Czech", "cs": "Czech",
        "romanian": "Romanian", "ro": "Romanian",
        "ukrainian": "Ukrainian", "uk": "Ukrainian",
        "hebrew": "Hebrew", "he": "Hebrew",
        "farsi": "Farsi", "fa": "Farsi",
        "pashto": "Pashto", "ps": "Pashto",
        "serbian": "Serbian", "sr": "Serbian",
        "malay": "Malay", "ms": "Malay",
        "indonesian": "Indonesian", "id": "Indonesian",
    }

    language_pattern = r'\b(' + "|".join(language_map.keys()) + r')\b'
    matches = re.findall(language_pattern, default_caption, re.IGNORECASE)

    if not matches:
        return "Not-Sure"

    detected_languages = set()
    for match in matches:
        detected_languages.add(language_map[match.lower()])

    return ", ".join(sorted(detected_languages, key=str.lower))


# টেস্ট
print(extract_language("Available in bn, ba, Bangla"))
# Output: Bangla, Bengali
print(extract_language("Dubbed in Bengali and Bangla"))
# Output: Bangla, Bengali


def extract_year(default_caption):
    match = re.search(r'\b(19\d{2}|20\d{2})\b', default_caption)
    return match.group(1) if match else None

# রিট্রাই সীমা (None দিলে অসীমান্ত রিট্রাই, কিন্তু প্রোডাকশনে ভুল হতে পারে)
RETRY_LIMIT = 5

@Client.on_message(filters.channel)
async def reCap(bot, message):
    chnl_id = message.chat.id
    if await is_chnl_banned(chnl_id): # <-- এই লাইনটি যোগ করুন
        return                        # <-- এই লাইনটি যোগ করুন
    default_caption = message.caption or ""     # None হলে খালি স্ট্রিং
    if message.media:
        for file_type in ("video", "audio", "document", "voice"):
            obj = getattr(message, file_type, None)
            if obj:
                # file_name পাওয়া গেলে ব্যবহার, নাহলে caption (প্রথম লাইন) ব্যবহার
                file_name = getattr(obj, "file_name", None)
                if not file_name or not str(file_name).strip():
                    # caption থেকে প্রথম লাইনের টেক্সট নিন (আর যদি সেটা ফাঁকা হয়, fallback বানান)
                    cap_first_line = default_caption.split("\n", 1)[0].strip() if default_caption else ""
                    if cap_first_line:
                        file_name = cap_first_line
                    else:
                        unique = getattr(obj, "file_unique_id", None) or str(message.message_id)
                        file_name = f"{file_type}_{unique}"

                # sanitize করে ফেলুন (ব্যবহারযোগ্য নাম)
                file_name = re.sub(r"@\w+\s*", "", str(file_name))
                file_name = file_name.replace("_", " ").replace(".", " ").strip()
                if len(file_name) > 200:  # অতিরিক্ত লম্বা হলে ছেটিয়ে দিন
                    file_name = file_name[:200].rsplit(" ", 1)[0]

                file_size = getattr(obj, "file_size", 0)
                language = extract_language(default_caption)
                year = extract_year(default_caption)
                cap_dets = await chnl_ids.find_one({"chnl_id": chnl_id})

                if cap_dets:
                    replaced_caption = cap_dets["caption"].format(
                        file_name=file_name,
                        file_size=get_size(file_size),
                        default_caption=default_caption,
                        language=language,
                        year=year
                    )
                else:
                    replaced_caption = DEF_CAP.format(
                        file_name=file_name,
                        file_size=get_size(file_size),
                        default_caption=default_caption,
                        language=language,
                        year=year
                    )

                # FloodWait সহ নিরাপদ এডিট (রিট্রাই লিমিট সহ)
                retries = 0
                success = False
                while True:
                    try:
                        await message.edit(replaced_caption)
                        success = True
                        break
                    except FloodWait as e:
                        # Pyrogram বিভিন্ন ভার্সনে attribute ভিন্ন হতে পারে; তাই দুটোই চেক করছি
                        wait = getattr(e, "value", None) or getattr(e, "x", None) or 30
                        print(f"[FloodWait] waiting {wait} seconds before retry...")
                        await asyncio.sleep(wait)
                        retries += 1
                        if RETRY_LIMIT is not None and retries >= RETRY_LIMIT:
                            print(f"[FloodWait] reached retry limit ({RETRY_LIMIT}). Giving up for this message.")
                            break
                        # লুপে ফিরে গিয়ে আবার চেষ্টা হবে
                    except Exception as ex:
                        print(f"[ERROR] while editing message: {ex}")
                        break

                # আপনি চাইলে success অনুযায়ী লগ/ইনফো পাঠাতে পারেন
    return


# Size conversion function
def get_size(size):
    units = ["Bytes", "Kʙ", "Mʙ", "Gʙ", "Tʙ", "Pʙ", "Eʙ"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units) - 1:  # Changed the condition to stop at the last unit
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])


@Client.on_callback_query(filters.regex(r'^start'))
async def start(bot, query):
    await query.message.edit_text(
        text=script.START_TXT.format(query.from_user.mention),  
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("➕️ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ➕️", url=f"https://t.me/Auto_Caption_Prime_Bot?startchannel=true")
                ],[
                InlineKeyboardButton("Hᴇʟᴘ", callback_data="help"),
                InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="about")
            ],[
                InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/PrimeXBots"),
                InlineKeyboardButton("💬 ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ 📜", url=r"https://t.me/Prime_Support_Group")
            ],[                
                InlineKeyboardButton("☆💫 𝗖𝗥𝗘𝗔𝗧𝗢𝗥 💫☆", url=r"https://t.me/Prime_Nayem")
            ]]
        ),
        disable_web_page_preview=True
)

@Client.on_callback_query(filters.regex(r'^help'))
async def help(bot, query):
    await query.message.edit_text(
        text=script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('About', callback_data='about')
            ],[
            InlineKeyboardButton('↩ ʙᴀᴄᴋ', callback_data='start')
            ]]
        ),
        disable_web_page_preview=True    
)

@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    await query.message.edit_text(
        text=script.ABOUT_TXT,
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ❓', callback_data='help')
            ],[
            InlineKeyboardButton('↩ ʙᴀᴄᴋ', callback_data='start')
            ],[
            InlineKeyboardButton('🧑‍💻 ꜱᴏᴜʀᴄᴇ ᴄoᴅᴇ 🧑‍💻', callback_data='source_prime')
            ]]
        ),
        disable_web_page_preview=True 
)


@Client.on_callback_query()
async def cb_handler(client, query):
    user_id = query.from_user.id
    if query.data == "closes":
        try:
            await query.message.delete()
        except Exception:
            await query.answer("⚠️ Cannot delete message.", show_alert=True)
        return  # exit early

    elif query.data == "source_prime":   # ← নতুন callback_data
        try:
            # প্রথমে আগের মেসেজ ডিলিট হবে
            await query.message.delete()
        except Exception:
            pass

        # এখন নতুন করে ছবি + ক্যাপশন পাঠানো হবে
        await query.message.reply_photo(
            photo="https://i.postimg.cc/hvFZ93Ct/file-000000004188623081269b2440872960.png",
            caption=(
                f"👋 Hello Dear 👋,\n\n"
                "⚠️ ᴛʜɪꜱ ʙᴏᴛ ɪꜱ ᴀ ᴘʀɪᴠᴀᴛᴇ ꜱᴏᴜʀᴄᴇ ᴘʀᴏᴊᴇᴄᴛ\n\n"
                "ᴛʜɪs ʙᴏᴛ ʜᴀs ʟᴀsᴛᴇsᴛ ᴀɴᴅ ᴀᴅᴠᴀɴᴄᴇᴅ ꜰᴇᴀᴛᴜʀᴇs⚡️\n"
                "▸ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ꜱᴏᴜʀᴄᴇ ᴄoᴅᴇ oʀ ʟɪᴋᴇ ᴛʜɪꜱ ʙᴏᴛ ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ..!\n"
                "▸ ɪ ᴡɪʟʟ ᴄʀᴇᴀᴛᴇ ᴀ ʙᴏᴛ ꜰᴏʀ ʏᴏᴜ oʀ ꜱᴏᴜʀᴄᴇ ᴄoᴅᴇ\n"
                "⇒ ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ - ♚ ᴀᴅᴍɪɴ ♚."
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("♚ ᴀᴅᴍɪɴ ♚", url="https://t.me/Prime_Admin_Support_ProBot")],
                    [InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="closes")]
                ]
            )
    )
        
