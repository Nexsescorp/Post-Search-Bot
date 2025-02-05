from info import *
from utils import *
from client import User
from pyrogram import Client, filters

# Command to connect a channel to the group
@Client.on_message(filters.group & filters.command("connect"))
async def connect(bot, message):
    # Initial reply to indicate connection attempt
    m = await message.reply("Connecting...")

    try:
        # Get the bot's user info (for error messages)
        user = await User.get_me()
    except Exception as e:
        return await m.edit(f"❌ Failed to get bot info: {e}")

    try:
        # Retrieve group details
        group_data = await get_group(message.chat.id)
        owner_id   = group_data["user_id"]
        owner_name = group_data["user_name"]
        verified   = group_data["verified"]
        channels   = group_data["channels"].copy()
    except Exception:
        # If group data cannot be retrieved, leave the chat
        return await bot.leave_chat(message.chat.id)

    # Check if the command is issued by the group owner
    if message.from_user.id != owner_id:
        return await m.edit(f"Only {owner_name} can use this command 😁")

    # Check if the group is verified
    if not bool(verified):
        return await m.edit("This chat is not verified!\nUse /verify to verify your group.")

    # Parse the channel ID from the command
    try:
        channel_id = int(message.command[-1])
        if channel_id in channels:
            return await m.edit("This channel is already connected! You can't connect it again.")
        # Add the new channel ID to the list
        channels.append(channel_id)
    except Exception:
        return await m.edit("❌ Incorrect format!\nUse `/connect ChannelID`")

    try:
        # Get chat details for the channel and the group
        channel_chat = await bot.get_chat(channel_id)
        group_chat   = await bot.get_chat(message.chat.id)
        c_link = channel_chat.invite_link
        g_link = group_chat.invite_link

        # Attempt to join the channel using the bot user
        await User.join_chat(c_link)
    except Exception as e:
        # If error indicates that the user is already a participant, we ignore it.
        if "already a participant" not in str(e):
            error_text = (
                f"❌ Error: `{e}`\nMake sure I'm admin in that channel and this group with all permissions, "
                f"and {(user.username or user.mention)} is not banned there."
            )
            return await m.edit(error_text)

    # Update the group record with the new channels list
    await update_group(message.chat.id, {"channels": channels})
    await m.edit(f"✅ Successfully connected to [{channel_chat.title}]({c_link})!", disable_web_page_preview=True)

    # Log the new connection
    log_text = (
        f"#NewConnection\n\nUser: {message.from_user.mention}\n"
        f"Group: [{group_chat.title}]({g_link})\n"
        f"Channel: [{channel_chat.title}]({c_link})"
    )
    await bot.send_message(chat_id=LOG_CHANNEL, text=log_text)


# Command to disconnect a channel from the group
@Client.on_message(filters.group & filters.command("disconnect"))
async def disconnect(bot, message):
    m = await message.reply("Please wait...")

    try:
        group_data = await get_group(message.chat.id)
        owner_id   = group_data["user_id"]
        owner_name = group_data["user_name"]
        verified   = group_data["verified"]
        channels   = group_data["channels"].copy()
    except Exception:
        return await bot.leave_chat(message.chat.id)

    if message.from_user.id != owner_id:
        return await m.edit(f"Only {owner_name} can use this command 😁")
    if not bool(verified):
        return await m.edit("This chat is not verified!\nUse /verify to verify your group.")

    try:
        channel_id = int(message.command[-1])
        if channel_id not in channels:
            return await m.edit("This channel is not connected yet or check the Channel ID.")
        channels.remove(channel_id)
    except Exception:
        return await m.edit("❌ Incorrect format!\nUse `/disconnect ChannelID`")

    try:
        channel_chat = await bot.get_chat(channel_id)
        group_chat   = await bot.get_chat(message.chat.id)
        c_link = channel_chat.invite_link
        g_link = group_chat.invite_link

        # Attempt to leave the channel
        await User.leave_chat(channel_id)
    except Exception as e:
        error_text = (
            f"❌ Error: `{e}`\nMake sure I'm admin in that channel and this group with all permissions, "
            f"and the owner is not banned there."
        )
        return await m.edit(error_text)

    await update_group(message.chat.id, {"channels": channels})
    await m.edit(f"✅ Successfully disconnected from [{channel_chat.title}]({c_link})!", disable_web_page_preview=True)

    # Log the disconnection
    log_text = (
        f"#DisConnection\n\nUser: {message.from_user.mention}\n"
        f"Group: [{group_chat.title}]({g_link})\n"
        f"Channel: [{channel_chat.title}]({c_link})"
    )
    await bot.send_message(chat_id=LOG_CHANNEL, text=log_text)


# Command to list all channel connections of the group
@Client.on_message(filters.group & filters.command("connections"))
async def connections(bot, message):
    try:
        group_data = await get_group(message.chat.id)
        owner_id   = group_data["user_id"]
        owner_name = group_data["user_name"]
        channels   = group_data["channels"]
        f_sub      = group_data.get("f_sub")
    except Exception as e:
        return await message.reply(f"❌ Error retrieving group info: {e}")

    if message.from_user.id != owner_id:
        return await message.reply(f"Only {owner_name} can use this command 😁")
    if not channels:
        return await message.reply("This group is currently not connected to any channels!\nConnect one using /connect")

    text = "This group is currently connected to:\n\n"
    for channel_id in channels:
        try:
            channel_chat = await bot.get_chat(channel_id)
            channel_name = channel_chat.title
            channel_link = channel_chat.invite_link
            text += f"🔗 Connected Channel - [{channel_name}]({channel_link})\n"
        except Exception as e:
            # Log individual channel errors instead of interrupting the process
            text += f"\n❌ Error retrieving channel {channel_id}: `{e}`"

    if f_sub:
        try:
            f_chat  = await bot.get_chat(f_sub)
            f_title = f_chat.title
            f_link  = f_chat.invite_link
            text += f"\nFSub: [{f_title}]({f_link})"
        except Exception as e:
            text += f"\n❌ Error retrieving FSub ({f_sub}): `{e}`"

    await message.reply(text=text, disable_web_page_preview=True)
   
       
       
