from info import *
from utils import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.group & filters.command("verify"))
async def verify_request(bot, message):
    """
    Handles the '/verify' command in group chats.
    Retrieves group details, validates the requester, and sends a verification
    request to the designated log channel.
    """
    try:
        # Attempt to get group details using your helper function.
        group = await get_group(message.chat.id)
        user_id = group["user_id"]
        user_name = group["user_name"]
        verified = group["verified"]
    except Exception as err:
        # If group details cannot be fetched, leave the chat.
        await bot.leave_chat(message.chat.id)
        return

    try:
        # Ensure the bot can get the user details.
        user = await bot.get_users(user_id)
    except Exception as err:
        return await message.reply(f"{user_name},\nPlease start me in PM.")

    # Only allow the designated user to use this command.
    if message.from_user.id != user_id:
        return await message.reply(f"Only {user.mention} can use this command 😁")

    # If already verified, notify and exit.
    if verified:
        return await message.reply("This group is already verified!!")

    try:
        # Fetch the group's invite link.
        chat = await bot.get_chat(message.chat.id)
        link = chat.invite_link
    except Exception as err:
        return await message.reply("Make me admin with all permissions!")

    # Prepare the verification request message.
    text = (
        "#NewRequest\n\n"
        f"User: {message.from_user.mention}\n"
        f"User ID: `{message.from_user.id}`\n"
        f"Group: [{message.chat.title}]({link})\n"
        f"Group ID: `{message.chat.id}`\n"
    )

    # Create the inline keyboard for approval/decline.
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"verify_approve_{message.chat.id}"),
            InlineKeyboardButton("❌ Decline", callback_data=f"verify_decline_{message.chat.id}")
        ]
    ])

    # Send the verification request to the log channel.
    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=text,
        disable_web_page_preview=True,
        reply_markup=markup
    )

    # Notify the user that the request has been sent.
    await message.reply("Verification request sent ✅\nWe will notify you when it is approved.")


@Client.on_callback_query(filters.regex(r"^verify"))
async def handle_verify_callback(bot, callback_query):
    """
    Handles the callback queries for verifying or declining a verification request.
    """
    try:
        # Extract action and chat_id from the callback data.
        data_parts = callback_query.data.split("_")
        action = data_parts[1]
        chat_id = int(data_parts[-1])
    except (IndexError, ValueError) as err:
        return await callback_query.answer("Invalid callback data", show_alert=True)

    # Retrieve group information.
    group = await get_group(chat_id)
    group_name = group.get("name")
    user_id = group.get("user_id")

    if action == "approve":
        # Update group verification status.
        await update_group(chat_id, {"verified": True})
        photo_url = "https://telegra.ph/file/a706afc296de6da2a40c8.jpg"
        caption = f"<b>Your verification request for {group_name} has been approved ✅</b>"
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎪 Subscribe to my YT channel 🎪", url="https://youtube.com/@RahulReviews")]
        ])
        # Notify the group owner with a photo and caption.
        await bot.send_photo(
            chat_id=user_id,
            photo=photo_url,
            caption=caption,
            reply_markup=markup
        )
        # Update the original message to indicate approval.
        new_text = callback_query.message.text_html.replace("#NewRequest", "#Approved")
        await callback_query.message.edit(new_text)
    elif action == "decline":
        # Delete the group entry and notify the user of the decline.
        await delete_group(chat_id)
        await bot.send_message(
            chat_id=user_id,
            text=f"Your verification request for {group_name} has been declined 😐 Please contact admin."
        )
    else:
        await callback_query.answer("Unknown action", show_alert=True)

                          
