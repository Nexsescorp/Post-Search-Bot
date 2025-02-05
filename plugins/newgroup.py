from info import LOG_CHANNEL  # import specific names instead of *
from utils import add_group
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.group & filters.new_chat_members)
async def new_group_handler(client: Client, message):
    """
    When new members join a group, check if the bot is among them.
    If so, register the group, send a welcome message with instructions,
    log the group details to a log channel, and delete the welcome message
    after a delay.
    """
    bot_id = (await client.get_me()).id
    new_member_ids = [user.id for user in message.new_chat_members]

    if bot_id in new_member_ids:
        # Register the group using a utility function.
        await add_group(
            group_id=message.chat.id,
            group_name=message.chat.title,
            user_name=message.from_user.first_name,
            user_id=message.from_user.id,
            channels=[],
            f_sub=False,
            verified=False
        )

        # Compose the welcome message text.
        welcome_text = (
            f"<b>☤ Thank you for adding me in {message.chat.title}\n\n"
            f"🤖 Don't forget to make me admin 🤖\n\n"
            f"♻️ Please get access by using the /verify command\n\n"
            f"🕵️ If you have any doubt, clear it using the buttons below</b>"
        )

        # Build the inline keyboard for support and owner contact.
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🥷 Help 🥷", url="https://telegram.me/CodeXSupport")],
            [InlineKeyboardButton("🧑‍💻 Owner 🧑‍💻", url="https://telegram.me/CodeXBro")]
        ])

        # Send the welcome message.
        welcome_msg = await message.reply(
            text=welcome_text,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

        # Log the group details.
        log_text = (
            f"#NewGroup\n\n"
            f"Group: {message.chat.title}\n"
            f"GroupID: `{message.chat.id}`\n"
            f"AddedBy: {message.from_user.mention}\n"
            f"UserID: `{message.from_user.id}`"
        )
        await client.send_message(chat_id=LOG_CHANNEL, text=log_text)

        # Wait for 120 seconds, then delete the welcome message.
        await sleep(120)
        await welcome_msg.delete()
