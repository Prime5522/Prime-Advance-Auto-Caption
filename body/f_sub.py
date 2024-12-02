from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from info import *
from .database import insert

async def not_subscribed(_, client, message):
    user_id = int(message.from_user.id)
    await insert(user_id)
    if not FORCE_SUB:
        return False
    try:             
        user = await client.get_chat_member(FORCE_SUB, message.from_user.id) 
        if user.status == enums.ChatMemberStatus.BANNED:
            return True 
        else:
            return False                
    except UserNotParticipant:
        pass
    return True


@Client.on_message(filters.private & filters.create(not_subscribed))
async def forces_sub(client, message):
    buttons = [[InlineKeyboardButton(text="📢 ✇ Join Our Updates Channel ✇ 📢", url=f"https://t.me/{FORCE_SUB}") ]]
    text = ""
    photo_url = "https://envs.sh/CEG.jpg"  # এখানে আপনার ইমেজ লিংক ব্যবহার করুন

    try:
        silicon = await client.get_chat_member(FORCE_SUB, message.from_user.id)    
        if silicon.status == enums.ChatMemberStatus.BANNED:  # যদি ব্যবহারকারী ব্যান হয়ে থাকে                             
            return await client.send_message(message.from_user.id, text="Sᴏʀʀy Yᴏᴜ'ʀᴇ Bᴀɴɴᴇᴅ Tᴏ Uꜱᴇ Mᴇ")  
    except UserNotParticipant:  # যদি ব্যবহারকারী সদস্য না হয়                     
        return await message.reply_photo(
            photo=photo_url,  # এখানে ইমেজ লিংক দিবেন
            caption=text,  # মেসেজ টেক্সট
            reply_markup=InlineKeyboardMarkup(buttons)  # চ্যানেল যোগদানের বাটন
        )
    return await message.reply_photo(
        photo=photo_url,
        caption=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
