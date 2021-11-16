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

from pyrogram import Client, filters
from pyrogram.types import Message

from crosmusic.config import PMPERMIT, SUDO_USERS
from crosmusic.services.callsmusic import client as USER

PMSET = True
pchats = []


@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
    if PMPERMIT == "ENABLE":
        if PMSET:
            chat_id = message.chat.id
            if chat_id in pchats:
                return
            await USER.send_message(
                message.chat.id,
                "𝐇𝐚𝐥𝐥𝐨, 𝐒𝐚𝐲𝐚 𝐀𝐝𝐚𝐥𝐚𝐡 𝐋𝐚𝐲𝐚𝐧𝐚𝐧 𝐀𝐬𝐢𝐬𝐭𝐞𝐧 𝐌𝐮𝐬𝐢𝐜..\n\n ❗️ 𝐑𝐮𝐥𝐞𝐬:\n   - 𝐉𝐚𝐧𝐠𝐚𝐧 𝐒𝐩𝐚𝐦 𝐏𝐞𝐬𝐚𝐧 𝐃𝐢 𝐬𝐢𝐧𝐢 𝐊𝐧𝐭𝐥\n   - 𝐓𝐮𝐭𝐨𝐫𝐢𝐚𝐥 𝐂𝐚𝐫𝐚 𝐌𝐞𝐧𝐠𝐠𝐮𝐧𝐚𝐤𝐚𝐧 𝐁𝐨𝐭 𝐋𝐢𝐡𝐚𝐭 𝐃𝐢 @TurboMusicChnl 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 \n\n 👉 **𝐊𝐈𝐑𝐈𝐌 𝐋𝐈𝐍𝐊 𝐈𝐍𝐕𝐈𝐓𝐄 𝐆𝐑𝐎𝐔𝐏 𝐀𝐓𝐀𝐔 𝐔𝐒𝐄𝐑𝐍𝐀𝐌𝐄 𝐉𝐈𝐊𝐀 𝐔𝐒𝐄𝐑𝐁𝐎𝐓 𝐏𝐄𝐍𝐆𝐆𝐔𝐍𝐀 𝐓𝐈𝐃𝐀𝐊 𝐁𝐈𝐒𝐀 𝐉𝐎𝐈𝐍 𝐆𝐑𝐎𝐔𝐏 𝐀𝐍𝐃𝐀 𝐋𝐀𝐍𝐆𝐒𝐔𝐍𝐆 𝐁𝐈𝐒𝐀 𝐋𝐀𝐏𝐎𝐑 𝐊𝐄 𝐎𝐖𝐍𝐄𝐑 𝐁𝐎𝐓 ||| @Biarenakliatnyaaa.**\n\n 💡 𝐃𝐢𝐥𝐚𝐫𝐚𝐧𝐠: 𝐉𝐢𝐤𝐚 𝐀𝐧𝐝𝐚 𝐦𝐞𝐧𝐠𝐢𝐫𝐢𝐦 𝐩𝐞𝐬𝐚𝐧 𝐝𝐢 𝐬𝐢𝐧𝐢 𝐛𝐞𝐫𝐚𝐫𝐭𝐢 𝐚𝐝𝐦𝐢𝐧 𝐚𝐤𝐚𝐧 𝐦𝐞𝐥𝐢𝐡𝐚𝐭 𝐩𝐞𝐬𝐚𝐧 𝐀𝐧𝐝𝐚 𝐝𝐚𝐧 𝐛𝐞𝐫𝐠𝐚𝐛𝐮𝐧𝐠 𝐝𝐞𝐧𝐠𝐚𝐧 𝐨𝐛𝐫𝐨𝐥𝐚𝐧 𝐜𝐡𝐚𝐭\n    - 𝐉𝐚𝐧𝐠𝐚𝐧 𝐀𝐝𝐝 𝐆𝐮𝐚 𝐊𝐞 𝐆𝐫𝐨𝐮𝐩𝐬 𝐑𝐚𝐡𝐚𝐬𝐢𝐚 𝐋𝐚𝐡 𝐊𝐧𝐭𝐥.\n   - 𝐉𝐚𝐧𝐠𝐚𝐧 𝐁𝐚𝐠𝐢𝐤𝐚𝐧 𝐈𝐧𝐟𝐨 𝐏𝐫𝐢𝐛𝐚𝐝𝐢 𝐀𝐧𝐝𝐚 𝐃𝐢 𝐒𝐢𝐧𝐢 𝐍𝐠𝐞𝐧𝐭𝐨𝐭\n\n",
            )
            return


@Client.on_message(filters.command(["/pmpermit"]))
async def bye(client: Client, message: Message):
    if message.from_user.id in SUDO_USERS:
        global PMSET
        text = message.text.split(" ", 1)
        queryy = text[1]
        if queryy == "on":
            PMSET = True
            await message.reply_text("Pmpermit turned on")
            return
        if queryy == "off":
            PMSET = None
            await message.reply_text("Pmpermit turned off")
            return


@USER.on_message(filters.text & filters.private & filters.me)
async def autopmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if not chat_id in pchats:
        pchats.append(chat_id)
        await message.reply_text("Approoved to PM due to outgoing messages")
        return
    message.continue_propagation()


@USER.on_message(filters.command("a", [".", ""]) & filters.me & filters.private)
async def pmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if not chat_id in pchats:
        pchats.append(chat_id)
        await message.reply_text("Approoved to PM")
        return
    message.continue_propagation()


@USER.on_message(filters.command("da", [".", ""]) & filters.me & filters.private)
async def rmpmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if chat_id in pchats:
        pchats.remove(chat_id)
        await message.reply_text("Dispprooved to PM")
        return
    message.continue_propagation()
