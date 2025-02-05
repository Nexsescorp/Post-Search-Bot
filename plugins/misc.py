from info import script
from utils import add_user, get_groups, get_users  # import only what is needed
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Helper to build the main keyboard for the /start command and home callback
def build_main_keyboard(user_mention: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            '⇄  Add me to your group  ⇄',
            url='https://telegram.me/RahulReviewsYT'
        )],
        [InlineKeyboardButton("Help", url="http://telegram.me/CodeXSupport"),
         InlineKeyboardButton("About", callback_data="misc_help")],
        [InlineKeyboardButton('❂ Our Updates Channel ❂', url='http://telegram.me/RahulReviewsYT')]
    ])

# /start command handler
@Client.on_message(filters.command("start") & ~filters.channel)
async def start_command(client: Client, message):
    await add_user(message.from_user.id, message.from_user.first_name)
    await message.reply(
        text=script.START.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=build_main_keyboard(message.from_user.mention)
    )

# /help command handler
@Client.on_message(filters.command("help"))
async def help_command(client: Client, message):
    await message.reply(
        text=script.HELP,
        disable_web_page_preview=True
    )

# /about command handler
@Client.on_message(filters.command("about"))
async def about_command(client: Client, message):
    me = await client.get_me()
    await message.reply(
        text=script.ABOUT.format(me.mention),
        disable_web_page_preview=True
    )

# /stats command handler (admin only)
@Client.on_message(filters.command("stats") & filters.user(ADMIN))
async def stats_command(client: Client, message):
    g_count, _ = await get_groups()
    u_count, _ = await get_users()
    await message.reply(script.STATS.format(u_count, g_count))

# /id command handler
@Client.on_message(filters.command("id"))
async def id_command(client: Client, message):
    parts = [f"<b>➲ Chat ID:</b> `{message.chat.id}`"]
    if message.from_user:
        parts.append(f"<b>➲ Your ID:</b> `{message.from_user.id}`")
    if message.reply_to_message:
        if message.reply_to_message.from_user:
            parts.append(f"<b>➲ Replied User ID:</b> `{message.reply_to_message.from_user.id}`")
        if message.reply_to_message.forward_from:
            parts.append(f"<b>➲ Forwarded From User ID:</b> `{message.reply_to_message.forward_from.id}`")
        if message.reply_to_message.forward_from_chat:
            parts.append(f"<b>➲ Forwarded From Chat ID:</b> `{message.reply_to_message.forward_from_chat.id}`")
    await message.reply("\n".join(parts))

# Build keyboard for callback queries with the "misc" prefix
def build_misc_keyboard(data: str) -> InlineKeyboardMarkup:
    if data == "help":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton('🧑‍💻 Contact Owner', url='https://telegram.me/CodeXBro')],
            [InlineKeyboardButton("Back", callback_data="misc_home"),
             InlineKeyboardButton("Next", url="https://github.com/codexbots/Post-Search-Bot")]
        ])
    elif data == "about":
        return InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="misc_home")]])
    else:
        # For "home" and defaults, show the main keyboard.
        return build_main_keyboard("")

# Callback query handler for misc actions
@Client.on_callback_query(filters.regex(r"^misc"))
async def misc_callback(client: Client, callback_query):
    data = callback_query.data.split("_")[-1]
    if data == "home":
        await callback_query.message.edit(
            text=script.START.format(callback_query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=build_main_keyboard(callback_query.from_user.mention)
        )
    elif data == "help":
        await callback_query.message.edit(
            text=script.HELP,
            disable_web_page_preview=True,
            reply_markup=build_misc_keyboard("help")
        )
    elif data == "about":
        me = await client.get_me()
        await callback_query.message.edit(
            text=script.ABOUT.format(me.mention),
            disable_web_page_preview=True,
            reply_markup=build_misc_keyboard("about")
        )

# Handler for private text messages
@Client.on_message(filters.private & filters.text & filters.incoming)
async def private_message_handler(client: Client, message):
    content = message.text
    if content.startswith("/") or content.startswith("#"):
        return  # ignore commands/hashtags
    reply_text = (
        "<b>Hi,\n\nIf you want movies/series, click on the first button; "
        "or for any bot issue, click on the second button.</b>"
    )
    await message.reply_text(
        text=reply_text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Request Here", url="https://telegram.me/RahulReviewsYT")],
            [InlineKeyboardButton("🧑‍💻 Bot Owner", url="https://telegram.me/CodeXBro")]
        ])
    )
    await client.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<b>#MSG\n\nName: {message.from_user.first_name}\n\nID: {message.from_user.id}\n\nMessage: {content}</b>"
    )
