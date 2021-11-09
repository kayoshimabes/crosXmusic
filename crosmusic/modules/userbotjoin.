# Daisyxmusic (Telegram bot project )
# Copyright (C) 2021  Inukaasith

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant

from crosmusic.config import SUDO_USERS
from crosmusic.helpers.decorators import authorized_users_only, errors
from crosmusic.services.callsmusic import client as USER


@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>🙋‍♂️ 𝐓𝐚𝐦𝐛𝐚𝐡𝐤𝐚𝐧 𝐬𝐚𝐲𝐚 𝐬𝐞𝐛𝐚𝐠𝐚𝐢 𝐚𝐝𝐦𝐢𝐧 𝐠𝐫𝐮𝐩 𝐀𝐧𝐝𝐚 𝐭𝐞𝐫𝐥𝐞𝐛𝐢𝐡 𝐝𝐚𝐡𝐮𝐥𝐮</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "crosmusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "𝐒𝐚𝐲𝐚 𝐛𝐞𝐫𝐠𝐚𝐛𝐮𝐧𝐠 𝐝𝐢 𝐬𝐢𝐧𝐢 𝐬𝐞𝐩𝐞𝐫𝐭𝐢 𝐲𝐚𝐧𝐠 𝐀𝐧𝐝𝐚 𝐦𝐢𝐧𝐭𝐚")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>💡𝐩𝐞𝐦𝐛𝐚𝐧𝐭𝐮 𝐬𝐮𝐝𝐚𝐡 𝐚𝐝𝐚 𝐝𝐢 𝐨𝐛𝐫𝐨𝐥𝐚𝐧 𝐠𝐫𝐨𝐮𝐩𝐬 𝐀𝐧𝐝𝐚</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 𝐊𝐞𝐬𝐚𝐥𝐚𝐡𝐚𝐧 𝐊𝐨𝐧𝐭𝐨𝐥 🛑 \n User {user.first_name} 𝐭𝐢𝐝𝐚𝐤 𝐝𝐚𝐩𝐚𝐭 𝐛𝐞𝐫𝐠𝐚𝐛𝐮𝐧𝐠 𝐝𝐞𝐧𝐠𝐚𝐧 𝐠𝐫𝐮𝐩 𝐀𝐧𝐝𝐚 𝐤𝐚𝐫𝐞𝐧𝐚 𝐛𝐚𝐧𝐲𝐚𝐤𝐧𝐲𝐚 𝐩𝐞𝐫𝐦𝐢𝐧𝐭𝐚𝐚𝐧 𝐛𝐞𝐫𝐠𝐚𝐛𝐮𝐧𝐠 𝐮𝐧𝐭𝐮𝐤 𝐮𝐬𝐞𝐫𝐛𝐨𝐭! 𝐏𝐚𝐬𝐭𝐢𝐤𝐚𝐧 𝐩𝐞𝐧𝐠𝐠𝐮𝐧𝐚 𝐭𝐢𝐝𝐚𝐤 𝐝𝐢𝐛𝐚𝐧𝐧 𝐝𝐢 𝐠𝐫𝐮𝐩."
            "\n\nOr 𝐭𝐚𝐦𝐛𝐚𝐡𝐤𝐚𝐧 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐜𝐞 𝐬𝐞𝐜𝐚𝐫𝐚 𝐦𝐚𝐧𝐮𝐚𝐥 𝐤𝐞 𝐆𝐫𝐮𝐩 𝐀𝐧𝐝𝐚 𝐝𝐚𝐧 𝐜𝐨𝐛𝐚 𝐥𝐚𝐠𝐢</b>",
        )
        return
    await message.reply_text(
        "<b>💡𝐡𝐞𝐥𝐩𝐞𝐫 𝐮𝐬𝐞𝐫𝐛𝐨𝐭 𝐛𝐞𝐫𝐠𝐚𝐛𝐮𝐧𝐠 𝐝𝐞𝐧𝐠𝐚𝐧 𝐨𝐛𝐫𝐨𝐥𝐚𝐧 𝐠𝐫𝐨𝐮𝐩𝐬 𝐀𝐧𝐝𝐚</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>𝐏𝐞𝐧𝐠𝐠𝐮𝐧𝐚 𝐭𝐢𝐝𝐚𝐤 𝐝𝐚𝐩𝐚𝐭 𝐦𝐞𝐧𝐢𝐧𝐠𝐠𝐚𝐥𝐤𝐚𝐧 𝐠𝐫𝐮𝐩 𝐀𝐧𝐝𝐚! 𝐌𝐮𝐧𝐠𝐤𝐢𝐧 𝐦𝐞𝐧𝐮𝐧𝐠𝐠𝐮 𝐒𝐞𝐬𝐞𝐨𝐫𝐚𝐧𝐠 𝐘𝐚𝐧𝐠𝐠 𝐭𝐢𝐝𝐚𝐤 𝐩𝐚𝐬𝐭𝐢."
            "\n\nOr 𝐬𝐞𝐜𝐚𝐫𝐚 𝐦𝐚𝐧𝐮𝐚𝐥 𝐦𝐞𝐧𝐞𝐧𝐝𝐚𝐧𝐠 𝐬𝐚𝐲𝐚 𝐝𝐚𝐫𝐢 𝐤𝐞 𝐆𝐫𝐮𝐩 𝐀𝐧𝐝𝐚</b>",
        )
        return


@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left = 0
        failed = 0
        lol = await message.reply("Assistant Leaving all chats")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left + 1
                await lol.edit(
                    f"𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐌𝐞𝐧𝐢𝐧𝐠𝐠𝐚𝐥𝐤𝐚𝐧... 𝐁𝐲𝐞: {left} chats. Failed: {failed} chats."
                )
            except:
                failed = failed + 1
                await lol.edit(
                    f"𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐌𝐞𝐧𝐢𝐧𝐠𝐠𝐚𝐥𝐤𝐚𝐧... 𝐁𝐲𝐞: {left} chats. Failed: {failed} chats."
                )
            await asyncio.sleep(0.7)
        await client.send_message(
            message.chat.id, f"Left {left} chats. Failed {failed} chats."
        )


@Client.on_message(
    filters.command(["userbotjoinchannel", "ubjoinc"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("Is chat even linked")
        return
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>🙋‍♂️ 𝐓𝐚𝐦𝐛𝐚𝐡𝐤𝐚𝐧 𝐬𝐚𝐲𝐚 𝐬𝐞𝐛𝐚𝐠𝐚𝐢 𝐚𝐝𝐦𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐀𝐧𝐝𝐚</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "crosmusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "𝐒𝐚𝐲𝐚 𝐛𝐞𝐫𝐠𝐚𝐛𝐮𝐧𝐠 𝐝𝐢 𝐬𝐢𝐧𝐢 𝐬𝐞𝐩𝐞𝐫𝐭𝐢 𝐲𝐚𝐧𝐠 𝐀𝐧𝐝𝐚 𝐦𝐢𝐧𝐭𝐚")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>💡𝐩𝐞𝐦𝐛𝐚𝐧𝐭𝐮 𝐬𝐮𝐝𝐚𝐡 𝐚𝐝𝐚 𝐝𝐢 𝐬𝐚𝐥𝐮𝐫𝐚𝐧 𝐀𝐧𝐝𝐚</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 𝐊𝐞𝐬𝐚𝐥𝐚𝐡𝐚𝐧 𝐊𝐨𝐧𝐭𝐨𝐥 🛑 \n User {user.first_name} 𝐭𝐢𝐝𝐚𝐤 𝐝𝐚𝐩𝐚𝐭 𝐛𝐞𝐫𝐠𝐚𝐛𝐮𝐧𝐠 𝐝𝐞𝐧𝐠𝐚𝐧 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐀𝐧𝐝𝐚 𝐤𝐚𝐫𝐞𝐧𝐚 𝐛𝐚𝐧𝐲𝐚𝐤𝐧𝐲𝐚 𝐩𝐞𝐫𝐦𝐢𝐧𝐭𝐚𝐚𝐧 𝐛𝐞𝐫𝐠𝐚𝐛𝐮𝐧𝐠 𝐮𝐧𝐭𝐮𝐤 𝐮𝐬𝐞𝐫𝐛𝐨𝐭! 𝐏𝐚𝐬𝐭𝐢𝐤𝐚𝐧 𝐩𝐞𝐧𝐠𝐠𝐮𝐧𝐚 𝐭𝐢𝐝𝐚𝐤 𝐝𝐢𝐛𝐚𝐧𝐧 𝐝𝐢 𝐜𝐡𝐚𝐧𝐧𝐞𝐥."
            "\n\nOr 𝐭𝐚𝐦𝐛𝐚𝐡𝐤𝐚𝐧 𝐚𝐬𝐢𝐬𝐭𝐞𝐧 𝐬𝐞𝐜𝐚𝐫𝐚 𝐦𝐚𝐧𝐮𝐚𝐥 𝐤𝐞 𝐆𝐫𝐮𝐩 𝐀𝐧𝐝𝐚 𝐝𝐚𝐧 𝐜𝐨𝐛𝐚 𝐥𝐚𝐠𝐢</b>",
        )
        return
    await message.reply_text(
        "<b>💡𝐡𝐞𝐥𝐩𝐞𝐫 𝐮𝐬𝐞𝐫𝐛𝐨𝐭 𝐛𝐞𝐫𝐠𝐚𝐛𝐮𝐧𝐠 𝐝𝐞𝐧𝐠𝐚𝐧 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐀𝐧𝐝𝐚</b>",
    )
