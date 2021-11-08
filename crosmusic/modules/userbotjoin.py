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
            "<b>🙋‍♂️ Tambahkan saya sebagai admin grup Anda terlebih dahulu</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "crosmusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "I joined here as you requested")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>helper already in your chat</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 кєѕαℓαнαη кσηтσℓ 🛑 \n User {user.first_name} тι∂αк ∂αραт вєяgαвυηg ∂єηgαη gяυρ αη∂α кαяєηα вαηуαкηуα ρєямιηтααη вєяgαвυηg υηтυк υѕєявσт! ραѕтιкαη ρєηggυηα тι∂αк ∂ιℓαяαηg ∂ι gяυρ."
            "\n\nOr тαмвαнкαη αѕιѕтєη ѕє¢αяα мαηυαℓ кє gяυρ αη∂α ∂αη ¢σвα ℓαgι</b>",
        )
        return
    await message.reply_text(
        "<b>✅ нєℓρєя υѕєявσт вєяgαвυηg ∂єηgαη σвяσℓαη gяσυρѕ αη∂α</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>ρєηggυηα тι∂αк ∂αραт мєηιηggαℓкαη gяυρ αη∂α! мυηgкιη мєηυηggυ кєтι∂αкραѕтιαη."
            "\n\nOr ѕє¢αяα нαℓυѕ мєηєη∂αηg ѕαуα ∂αяι кє gяυρ αη∂α</b>",
        )
        return


@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left = 0
        failed = 0
        lol = await message.reply("αѕιѕтєη мєηιηggαℓкαη ѕємυα σвяσℓαη вує👋")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left + 1
                await lol.edit(
                    f"αѕѕιѕтαηт ℓєανιηg... ℓєƒт: {left} chats. Failed: {failed} chats."
                )
            except:
                failed = failed + 1
                await lol.edit(
                    f"αѕѕιѕтαηт ℓєανιηg... ℓєƒт: {left} chats. Failed: {failed} chats."
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
        await message.reply("αραкαн σвяσℓαη ѕυαяα тєℓαн тєянυвυηg?")
        return
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>🙋‍♂️ тαмвαнкαη ѕαуα ѕєвαgαι α∂мιη ѕαℓυяαη αη∂α тєяℓєвιн ∂αнυℓυ</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "crosmusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "I joined here as you requested")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>ρємвαηтυ ѕυ∂αн α∂α ∂ι ¢нαηηєℓ αη∂α</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 кєѕαℓαнαη кσηтσℓ 🛑 \n User {user.first_name} тι∂αк ∂αραт вєяgαвυηg ∂єηgαη ѕαℓυяαη αη∂α кαяєηα вαηуαкηуα ρєямιηтααη вєяgαвυηg υηтυк υѕєявσт! ραѕтιкαη ρєηggυηα тι∂αк ∂ιвαηη ∂ι ѕαℓυяαη."
            "\n\nOr тαмвαнкαη αѕιѕтєη ѕє¢αяα мαηυαℓ кє gяυρ αη∂α ∂αη ¢σвα ℓαgι</b>",
        )
        return
    await message.reply_text(
        "<b>✅ нєℓρєя υѕєявσт вєяgαвυηg ∂єηgαη ¢нαηηєℓ αη∂α</b>",
    )
