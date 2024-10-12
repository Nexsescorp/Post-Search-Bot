from info import *
from utils import *
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

@Client.on_message(filters.command("start") & ~filters.channel)
async def start(bot, message):
    await add_user(message.from_user.id, message.from_user.first_name)
    await message.reply(text=script.START.format(message.from_user.mention),
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⇄  ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ  ⇄', url=f'https://t.me/Nexses_Corporation')
            ],[InlineKeyboardButton("ʜᴇʟᴘ", url="http://telegram.me/Nexses"),

InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="misc_help")],[InlineKeyboardButton('❂   ᴏᴜʀ  ᴜᴘᴅᴀᴛᴇꜱ  ᴄʜᴀɴɴᴇʟ   ❂', url=f'https://t.me/Nexses_Corporation')]]))  
@Client.on_message(filters.command("help"))
async def help(bot, message):
    await message.reply(text=script.HELP,
                        disable_web_page_preview=True)

@Client.on_message(filters.command("about"))
async def about(bot, message):
    await message.reply(text=script.ABOUT.format((await bot.get_me()).mention),
                        disable_web_page_preview=True)

@Client.on_message(filters.command("stats") & filters.user(ADMIN))
async def stats(bot, message):
    g_count, g_list = await get_groups()
    u_count, u_list = await get_users()
    await message.reply(script.STATS.format(u_count, g_count))

@Client.on_message(filters.command("id"))
async def id(bot, message):
    text = f"<b>➲  ᴄʜᴀᴛ ɪᴅ:-</b>  `{message.chat.id}`\n"
    if message.from_user:
       text += f"<b>➲  ʏᴏᴜʀ ɪᴅ:-</b> `{message.from_user.id}`\n"
    if message.reply_to_message:
       if message.reply_to_message.from_user:
          text += f"<b>➲  ʀᴇᴘʟɪᴇᴅ ᴜꜱᴇʀ ɪᴅ:-</b> `{message.reply_to_message.from_user.id}`\n"
       if message.reply_to_message.forward_from:
          text += f"<b>➲  ʀᴇᴘʟɪᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ꜰᴏʀᴡᴀʀᴅ ꜰʀᴏᴍ ᴜꜱᴇʀ ɪᴅ:-</b> `{message.reply_to_message.forward_from.id}`\n"
       if message.reply_to_message.forward_from_chat:
          text += f"<b>➲  ʀᴇᴘʟɪᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ꜰᴏʀᴡᴀʀᴅ ꜰʀᴏᴍ ᴄʜᴀᴛ ɪᴅ:-</b> `{message.reply_to_message.forward_from_chat.id}\n`"
    await message.reply(text)

@Client.on_callback_query(filters.regex(r"^misc"))
async def misc(bot, update):
    data = update.data.split("_")[-1]
    if data=="home":
       await update.message.edit(text=script.START.format(update.from_user.mention),
                                 disable_web_page_preview=True,
                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⇄  Add Me To Your Grp ⇄', url=f'https://t.me/Nexses_Corporation')
            ],[InlineKeyboardButton("ʜᴇʟᴘ", url="http://telegram.me/Nexses"),

InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="misc_help")],[InlineKeyboardButton(' Our Update Channel ', url=f'https://t.me/Nexses_Corporation')]])) 
    elif data=="help":
       await update.message.edit(text=script.HELP, 
                                 disable_web_page_preview=True,
                                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🧑‍💻   ᴄᴏɴᴛᴀᴄᴛ  ᴛᴏ  ᴏᴡɴᴇʀ   🧑‍💻',url='https://telegram.me/Nexses')],[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="misc_home"),InlineKeyboardButton("ɴᴇxᴛ", url="https://github.com/codexbots/Post-Search-Bot")]])) 


    elif data=="about":
        await update.message.edit(text=script.ABOUT.format((await bot.get_me()).mention), 
                                  disable_web_page_preview=True,
                                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="misc_home")]]))

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    content = message.text
    user = message.from_user.first_name
    user_id = message.from_user.id
    if content.startswith("/") or content.startswith("#"): return  # ignore commands and hashtags
    await message.reply_text(
         text="<b>ʜʏ,\n\nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴍᴏᴠɪᴇs / sᴇʀɪᴇs ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ꜰɪʀsᴛ ʙᴜᴛᴛᴏɴ ᴏʀ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ɪɴ ʙᴏᴛ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ sᴇᴄᴏɴᴅ ʙᴜᴛᴛᴏɴ</b>",   
         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝  ʀᴇǫᴜᴇsᴛ ʜᴇʀᴇ​ ", url=f"https://t.me/Nexses_Corporation")],[InlineKeyboardButton("🧑‍💻  ʙᴏᴛ ᴏᴡɴᴇʀ ", url=f"https://telegram.me/Nexses")]]), disable_web_page_preview=True
    )
    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<b>#𝐌𝐒𝐆\n\nNᴀᴍᴇ : {user}\n\nID : {user_id}\n\nMᴇssᴀɢᴇ : {content}</b>"
    )
