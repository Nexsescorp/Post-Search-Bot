from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import *
from utils import *
from time import time
from client import User
import asyncio

# Helper function for message sending
async def send_search_results(message, results, query=None):
    head = "<b>⇩  ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ʀᴇꜱᴜʟᴛꜱ  ⇩</b>\n\n"
    if results:
        return await message.reply_text(text=head + results, disable_web_page_preview=True)
    else:
        # Handle if no results found
        movies = await search_imdb(query)
        buttons = [InlineKeyboardButton(movie['title'], callback_data=f"recheck_{movie['id']}") for movie in movies]
        return await message.reply("𝗜 𝗰𝗼𝘂𝗹𝗱𝗻'𝘁 𝗳𝗶𝗻𝗱 𝗮𝗻𝘆𝘁𝗵𝗶𝗻𝗴 𝗿𝗲𝗹𝗮𝘁𝗲𝗱 𝘁𝗼 𝘁𝗵𝗮𝘁.\n𝗗𝗶𝗱 𝘆𝗼𝘂 𝗺𝗲𝗮𝗻 𝗮𝗻𝘆 𝗼𝗻𝗲 𝗼𝗳 𝘁𝗵𝗲𝘀𝗲 ??",
                                          reply_markup=InlineKeyboardMarkup([buttons]))

@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    # Ensure user is subscribed
    f_sub = await force_sub(bot, message)
    if not f_sub:
        return

    # Get channel list from group
    channels = (await get_group(message.chat.id))["channels"]
    if not channels:
        return

    # Handle search query
    query = message.text
    if query.startswith("/"):
        return  # Ignore commands

    results = ""
    try:
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                name = (msg.text or msg.caption).split("\n")[0]
                if name not in results:
                    results += f"<b>🎬 {name}\n {msg.link} </b>\n\n"
        await send_search_results(message, results, query)

        # Track and save the message for deletion
        _time = int(time()) + (15 * 60)
        await save_dlt_message(message, _time)
    except Exception as e:
        # Log any error that occurs
        print(f"Error processing search: {e}")

# Similar refactoring could be applied to other handlers, like recheck and request, to enhance readability.
