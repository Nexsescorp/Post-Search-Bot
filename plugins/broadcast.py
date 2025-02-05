import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from info import *
from utils import *

# Command to broadcast to users
@Client.on_message(filters.command('broadcast') & filters.user(ADMIN))
async def broadcast(bot, message):
    if not message.reply_to_message:
        return await message.reply("Use this command as a reply to any message!")

    m = await message.reply("Please wait...")

    count, users = await get_users()
    stats = "⚡ Broadcast Processing.."
    br_msg = message.reply_to_message
    total = count
    remaining = total
    success = 0
    failed = 0

    for user in users:
        chat_id = user["_id"]
        trying = await copy_msgs(br_msg, chat_id)
        
        if not trying:
            failed += 1
        else:
            success += 1
        remaining -= 1

        try:
            # Update the progress of broadcast
            await m.edit(script.BROADCAST.format(stats, total, remaining, success, failed))
        except Exception:
            pass

    stats = "✅ Broadcast Completed"
    await m.reply(script.BROADCAST.format(stats, total, remaining, success, failed))
    await m.delete()

# Command to broadcast to groups
@Client.on_message(filters.command('broadcast_groups') & filters.user(ADMIN))
async def grp_broadcast(bot, message):
    if not message.reply_to_message:
        return await message.reply("Use this command as a reply to any message!")

    m = await message.reply("Please wait...")

    count, groups = await get_groups()
    stats = "⚡ Broadcast Processing.."
    br_msg = message.reply_to_message
    total = count
    remaining = total
    success = 0
    failed = 0

    for group in groups:
        chat_id = group["_id"]
        trying = await grp_copy_msgs(br_msg, chat_id)

        if not trying:
            failed += 1
        else:
            success += 1
        remaining -= 1

        try:
            # Update the progress of group broadcast
            await m.edit(script.BROADCAST.format(stats, total, remaining, success, failed))
        except Exception:
            pass

    stats = "✅ Broadcast Completed"
    await m.reply(script.BROADCAST.format(stats, total, remaining, success, failed))
    await m.delete()

# Function to copy messages to a group
async def grp_copy_msgs(br_msg, chat_id):
    try:
        h = await br_msg.copy(chat_id)
        try:
            await h.pin()
        except Exception:
            pass
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await grp_copy_msgs(br_msg, chat_id)
    except Exception as e:
        await delete_group(chat_id)
        return False

# Function to copy messages to a user
async def copy_msgs(br_msg, chat_id):
    try:
        await br_msg.copy(chat_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await copy_msgs(br_msg, chat_id)
    except Exception as e:
        await delete_user(chat_id)
        return False

