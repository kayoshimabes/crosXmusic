# Daisyxmusic (Telegram bot project)
# Copyright (C) 2021  Inukaasith
# Copyright (C) 2021  TheHamkerCat (Python_ARQ)
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


import os
from os import path
from typing import Callable

import aiofiles
import aiohttp
import ffmpeg
import requests
import wget
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch

from crosmusic.config import ARQ_API_KEY
from crosmusic.config import BOT_NAME as bn
from crosmusic.config import DURATION_LIMIT
from crosmusic.config import UPDATES_CHANNEL as updateschannel
from crosmusic.config import que
from crosmusic.function.admins import admins as a
from crosmusic.helpers.admins import get_administrators
from crosmusic.helpers.channelmusic import get_chat_id
from crosmusic.helpers.decorators import authorized_users_only
from crosmusic.helpers.filters import command, other_filters
from crosmusic.helpers.gets import get_file_name
from crosmusic.services.callsmusic import callsmusic
from crosmusic.services.callsmusic import client as USER
from crosmusic.services.converter.converter import convert
from crosmusic.services.downloaders import youtube
from crosmusic.services.queues import queues

aiohttpsession = aiohttp.ClientSession()
chat_id = None
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)
DISABLED_GROUPS = []
useer = "NaN"


def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        else:
            await cb.answer("You ain't allowed!", show_alert=True)
            return

    return decorator


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", 
        format="s16le", 
        acodec="pcm_s16le", 
        ac=2, 
        ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("./etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((205, 550), f"Title: {title}", (51, 215, 255), font=font)
    draw.text((205, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((205, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (205, 670),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(filters.command("playlist") & filters.group & ~filters.edited)
async def playlist(client, message):
    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text("Player is idle")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "**Now Playing** in {}".format(message.chat.title)
    msg += "\n- " + now_playing
    msg += "\n- Req by " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "**Queue**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n- {name}"
            msg += f"\n- Req by {usr}\n"
    await message.reply_text(msg)


# ============================= Settings =========================================


def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.active_chats:
        # if chat.id in active_chats:
        stats = "Settings of **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "Volume : {}%\n".format(vol)
            stats += "Songs in queue : `{}`\n".format(len(que))
            stats += "Now Playing : **{}**\n".format(queue[0][0])
            stats += "Requested by : {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats


def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip"),
            ],
            [
                InlineKeyboardButton("Playlist 📖", "playlist"),
            ],
            [InlineKeyboardButton("❌ Close", "cls")],
        ]
    )
    return mar


@Client.on_message(filters.command("current") & filters.group & ~filters.edited)
async def ee(client, message):
    if message.chat.id in DISABLED_GROUPS:
        return
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        await message.reply(stats)
    else:
        await message.reply("тι∂αк α∂α ιηѕтαηѕ ν¢ уαηg вєяʝαℓαη ∂αℓαм σвяσℓαη ιηι")


@Client.on_message(filters.command("player") & filters.group & ~filters.edited)
@authorized_users_only
async def settings(client, message):
    if message.chat.id in DISABLED_GROUPS:
        await message.reply("❗ρємυтαя мυѕιк ∂ιησηαктιƒкαη")
        return
    playing = None
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.active_chats:
        playing = True
    queue = que.get(chat_id)
    stats = updated_stats(message.chat, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))
        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("тι∂αк α∂α ιηѕтαηѕ ν¢ уαηg вєяʝαℓαη ∂αℓαм σвяσℓαη ιηι")


@Client.on_message(
    filters.command("musicplayer") & ~filters.edited & ~filters.bot & ~filters.private
)
@authorized_users_only
async def hfmm(_, message):
    global DISABLED_GROUPS
    try:
        message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text(
            "ѕαуα нαηуα мєηgєηαℓι `/musicplayer on` αη∂ /musicplayer `off σηℓу`"
        )
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await message.reply("`ρяσ¢єѕѕιηg...`")
        if not message.chat.id in DISABLED_GROUPS:
            await lel.edit("✅ ρємυтαя мυѕιк ѕυ∂αн ∂ιαктιƒкαη ∂ι σвяσℓαη gяσυρѕ ιηι")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(
            f"✅ ρємυтαя мυѕιк вєянαѕιℓ ∂ιαктιƒкαη υηтυк ρєηggυηα ∂αℓαм σвяσℓαη {message.chat.id}"
        )

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await message.reply("`ρяσ¢єѕѕιηg...`")

        if message.chat.id in DISABLED_GROUPS:
            await lel.edit("🚫 ρємυтαя мυѕιк ѕυ∂αн ∂ιмαтιкαη ∂αℓαм σвяσℓαη gяσυρѕ ιηι")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(
            f"🚫 ρємυтαя мυѕιк вєянαѕιℓ ∂ιησηαктιƒкαη υηтυк ρєηggυηα ∂αℓαм σвяσℓαη {message.chat.id}"
        )
    else:
        await message.reply_text(
            "ѕαуα нαηуα мєηgєηαℓι `/musicplayer on` αη∂ /musicplayer `off σηℓу`"
        )


@Client.on_callback_query(filters.regex(pattern=r"^(playlist)$"))
async def p_cb(b, cb):
    global que
    que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("ρємαιη ℓαgι ηgαηggυя")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "<b>Now Playing</b> in {}".format(cb.message.chat.title)
        msg += "\n- " + now_playing
        msg += "\n- Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Queue**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Req by {usr}\n"
        await cb.message.edit(msg)


@Client.on_callback_query(
    filters.regex(pattern=r"^(play|pause|skip|leave|puse|resume|menu|cls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    if (
        cb.message.chat.title.startswith("Channel Music: ")
        and chat.title[14:].isnumeric()
    ):
        chet_id = int(chat.title[13:])
    else:
        chet_id = cb.message.chat.id
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "pause":
        (
            await cb.answer("Music Paused!")
        ) if (
            callsmusic.pause(chet_id)
        ) else (
            await cb.answer("σвяσℓαη тι∂αк тєянυвυηg❗", show_alert=True)
        )
        await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply("play"))

    elif type_ == "resume":
        (
            await cb.answer("Music Resumed!")
        ) if (
            callsmusic.resume(chet_id)
        ) else (
            await cb.answer("σвяσℓαη тι∂αк тєянυвυηg❗", show_alert=True)
        )
        await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply("pause"))

    elif type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("ρємαιη ℓαgι ηgαηggυя")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Now Playing** in {}".format(cb.message.chat.title)
        msg += "\n- " + now_playing
        msg += "\n- Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Queue**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Req by {usr}\n"
        await cb.message.edit(msg)

    elif type_ == "resume":
        (
            await cb.answer("Music Resumed!")
        ) if (
            callsmusic.resume(chet_id)
        ) else (
            await cb.answer("σвяσℓαη тι∂αк тєянυвυηg αтαυ ѕυ∂αн ∂ιρυтαя❗", show_alert=True)
        )
            
    elif type_ == "puse":
        (
            await cb.answer("Music Paused!")
        ) if (
            callsmusic.pause(chet_id)
        ) else (
            await cb.answer("σвяσℓαη тι∂αк тєянυвυηg αтαυ ѕυ∂αн ∂ιʝє∂α❗", show_alert=True)
        )
            
    elif type_ == "cls":
        await cb.answer("Closed menu")
        await cb.message.delete()

    elif type_ == "menu":
        stats = updated_stats(cb.message.chat, qeue)
        await cb.answer("Menu opened")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "leave"),
                    InlineKeyboardButton("⏸", "puse"),
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏭", "skip"),
                ],
                [
                    InlineKeyboardButton("Playlist 📖", "playlist"),
                ],
                [InlineKeyboardButton("❌ Close", "cls")],
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)
        
    elif type_ == "skip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.active_chats:
            await cb.answer("σвяσℓαη тι∂αк тєянυвυηg❗", show_alert=True)
        else:
            queues.task_done(chet_id)
            if queues.is_empty(chet_id):
                callsmusic.stop(chet_id)
                await cb.message.edit("- No More Playlist..\n- Leaving VC!")
            else:
                await callsmusic.set_stream(
                    chet_id, 
                    queues.get(chet_id)["file"],
                )
                await cb.answer.reply_text("✅ <b>Skipped</b>")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    f"- Skipped track\n- Now Playing **{qeue[0][0]}**"
                )

    else:
        if chet_id in callsmusic.active_chats:
            try:
                queues.clear(chet_id)
            except QueueEmpty:
                pass

            await callsmusic.stop(chet_id)
            await cb.message.edit("вєянαѕιℓ мєηιηggαℓкαη σвяσℓαη вує кηтℓ🗑")
        else:
            await cb.answer("σвяσℓαη тι∂αк тєянυвυηg❗", show_alert=True)
            
     
@Client.on_message(command("play") & other_filters)
async def play(_, message: Message):
    global que
    global useer
    if message.chat.id in DISABLED_GROUPS:
        return
    lel = await message.reply("🔄 <b>ρяσ¢єѕѕιηg</b>")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>⚠️ ιηgαтℓαн υηтυк мєηαмвαнкαη ρємвαηтυ кє ¢нαηηєℓ αη∂α</b>",
                    )
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>🙋‍♂️ тαмвαнкαη ѕαуα ѕєвαgαι α∂мιη gяυρ αη∂α тєяℓєвιн ∂αнυℓυ</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "☕ ѕαуα вєяgαвυηg ∂єηgαη gяυρ ιηι υηтυк мємυтαя мυѕιк ∂ι ν¢g"
                    )
                    await lel.edit(
                        "<b>нєℓρєя υѕєявσт вєяgαвυηg ∂єηgαη σвяσℓαη gяσυρѕ αη∂α</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 кєѕαℓαнαη тυηggυ ∂υℓυ кηтℓ 🔴 \nUser {user.first_name} тι∂αк ∂αραт вєяgαвυηg ∂єηgαη gяυρ αη∂α кαяєηα вαηуαкηуα ρєямιηтααη υηтυк υѕєявσт! ραѕтιкαη ρєηggυηα тι∂αк ∂ιвαη ∂ι gяυρ."
                        "\n\nOr тαмвαнкαη αѕιѕтєη ѕє¢αяα мαηυαℓ кє gяυρ αη∂α ∂αη ¢σвα ℓαgι</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i> {user.first_name} υѕєявσт тι∂αк α∂α ∂αℓαм σвяσℓαη ιηι, мιηтα α∂мιη υηтυк мєηgιяιм /play ρєяιηтαн υηтυк ρєятαмα кαℓι αтαυ тαмвαнкαη {user.first_name} мαηυαℓℓу</i>"
        )
        return
    text_links = None
    await lel.edit("🔎 <b>ƒιη∂ιηg ѕσηg</b>")
    if message.reply_to_message:
        if message.reply_to_message.audio:
            pass
        entities = []
        if message.entities:
            entities += entities
        elif message.caption_entities:
            entities += message.caption_entities
        if message.reply_to_message:
            text = message.reply_to_message.text \
                or message.reply_to_message.caption
            if message.reply_to_message.entities:
                entities = message.reply_to_message.entities + entities
            elif message.reply_to_message.caption_entities:
                entities = message.reply_to_message.entities + entities
        else:
            text = message.text or message.caption

        urls = [entity for entity in entities if entity.type == 'url']
        text_links = [
            entity for entity in entities if entity.type == 'text_link'
        ]
    else:
        urls = None
    if text_links:
        urls = True
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❌ νι∂єσ ℓєвιн ραηʝαηg ∂αяι {DURATION_LIMIT} minute(s) тι∂αк ∂ιρєявσℓєнкαη вєямαιη!"
            )
            return
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📖 Playlist", callback_data="playlist"),
                    InlineKeyboardButton("Menu ⏯ ", callback_data="menu"),
                ],
                [InlineKeyboardButton(text="❌ Close", callback_data="cls")],
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/85e95989bda69d4919b65.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file = await convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("🎵 <b>ρяσ¢єѕѕιηg</b>")
        ydl_opts = {"format": "bestaudio/best"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "ℓαgυ тι∂αк ∂ιтємυкαη кηтℓ. ¢σвα ¢αяι ℓαgυ уαηg уαηg вєηєя ηαρα кηтℓ."
            )
            print(str(e))
            return
        try:
            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60
            if (dur / 60) > DURATION_LIMIT:
                await lel.edit(
                    f"❌ νι∂єσ ℓєвιн ραηʝαηg ∂αяι {DURATION_LIMIT} minutes тι∂αк ∂ιρєявσℓєнкαη вєямαιη!"
                )
                return
        except:
            pass
        dlurl = url
        dlurl = dlurl.replace("youtube", "youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📖 Playlist", callback_data="playlist"),
                    InlineKeyboardButton("Menu ⏯ ", callback_data="menu"),
                ],
                [
                    InlineKeyboardButton(text="🎬 YouTube", url=f"{url}"),
                    InlineKeyboardButton(text="Download 📥", url=f"{dlurl}"),
                ],
                [InlineKeyboardButton(text="❌ Close", callback_data="cls")],
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file = await convert(youtube.download(url))
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await lel.edit("🎵 **ρяσ¢єѕѕιηg**")
        ydl_opts = {"format": "bestaudio/best"}

        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
        except:
            await lel.edit("✨ вєяι αкυ ѕєѕυαтυ υηтυк ∂ιмαιηкαη")
        # Looks like hell. Aren't it?? FUCK OFF
        try:
            toxxt = "**__ριℓιн ∂αƒтαя ℓαgυ уαηg ιηgιη ∂ι ∂єηgαя__💡**\n\n"
            j = 0
            useer = user_name
            emojilist = [
                "1️⃣",
                "2️⃣",
                "3️⃣",
                "4️⃣",
                "5️⃣",
            ]

            while j < 5:
                toxxt += f"{emojilist[j]} <b>Title - [{results[j]['title']}](https://youtube.com{results[j]['url_suffix']})</b>\n"
                toxxt += f" ├ ⌚<b>∂υяαтιση</b> - {results[j]['duration']}\n"
                toxxt += f" ├ 🩸<b>νιєωѕ</b> - {results[j]['views']}\n"
                toxxt += f" └ ✨<b>¢нαηηєℓ</b> - {results[j]['channel']}\n\n"

                j += 1
            koyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "1️⃣", callback_data=f"plll 0|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "2️⃣", callback_data=f"plll 1|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "3️⃣", callback_data=f"plll 2|{query}|{user_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "4️⃣", callback_data=f"plll 3|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "5️⃣", callback_data=f"plll 4|{query}|{user_id}"
                        ),
                    ],
                    [InlineKeyboardButton(text="❌ Close", callback_data="cls")],
                ]
            )
            await lel.edit(toxxt, reply_markup=koyboard, disable_web_page_preview=True)
            # WHY PEOPLE ALWAYS LOVE PORN ?? (A point to think)
            return
            # Returning to pornhub
        except:
            await lel.edit("❗тι∂αк α∂α нαѕιℓ уαηg ¢υкυρ υηтυк ∂ιριℓιн.. мυℓαι вєямαιη ℓαηgѕυηg..")

            # print(results)
            try:
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:40]
                thumbnail = results[0]["thumbnails"][0]
                thumb_name = f"thumb{title}.jpg"
                thumb = requests.get(thumbnail, allow_redirects=True)
                open(thumb_name, "wb").write(thumb.content)
                duration = results[0]["duration"]
                results[0]["url_suffix"]
                views = results[0]["views"]

            except Exception as e:
                await lel.edit(
                    "ℓαgυ тι∂αк ∂ιтємυкαη кηтℓ. ¢σвα ¢αяι ℓαgυ уαηg уαηg вєηєя ηαρα кηтℓ."
                )
                print(str(e))
                return
            try:
                secmul, dur, dur_arr = 1, 0, duration.split(":")
                for i in range(len(dur_arr) - 1, -1, -1):
                    dur += int(dur_arr[i]) * secmul
                    secmul *= 60
                if (dur / 60) > DURATION_LIMIT:
                    await lel.edit(
                        f"❌ νι∂єσ ℓєвιн ραηʝαηg ∂αяι {DURATION_LIMIT} minutes тι∂αк ∂ιρєявσℓєнкαη вєямαιη!"
                    )
                    return
            except:
                pass
            dlurl = url
            dlurl = dlurl.replace("youtube", "youtubepp")
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📖 Playlist", callback_data="playlist"),
                        InlineKeyboardButton("Menu ⏯ ", callback_data="menu"),
                    ],
                    [
                        InlineKeyboardButton(text="🎬 YouTube", url=f"{url}"),
                        InlineKeyboardButton(text="Download 📥", url=f"{dlurl}"),
                    ],
                    [InlineKeyboardButton(text="❌ Close", callback_data="cls")],
                ]
            )
            requested_by = message.from_user.first_name
            await generate_cover(requested_by, title, views, duration, thumbnail)
            file = await convert(youtube.download(url))
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.active_chats:
        position = await queues.put(chat_id, file=file)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"#⃣ ℓαgυ уαηg ℓυ мιηтα <b>queued</b> ℓαgι αηтяι ∂ι ρσѕιѕι {position}!",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            await callsmusic.set_stream(chat_id, file)
        except:
            message.reply("❌ ραηggιℓαη gяυρ тι∂αк тєянυвυηg αтαυ ѕαуα тι∂αк ∂αραт вєяgαвυηg")
            return
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="▶️ <b>Playing</b> ιηι ℓαgυ уαηg ∂ιмιηтα σℓєн {} via Youtube Music 😎".format(
                message.from_user.mention()
            ),
        )
        os.remove("final.png")
        return await lel.delete()


@Client.on_message(filters.command("ytplay") & filters.group & ~filters.edited)
async def ytplay(_, message: Message):
    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    lel = await message.reply("🔄 <b>ρяσ¢єѕѕιηg</b>")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>⚠️ ιηgαтℓαн υηтυк мєηαмвαнкαη ρємвαηтυ кє ѕαℓυяαη αη∂α</b>",
                    )
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>🙋‍♂️ тαмвαнкαη ѕαуα ѕєвαgαι α∂мιη gяυρ αη∂α тєяℓєвιн ∂αнυℓυ</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "✅ ѕαуα вєяgαвυηg ∂єηgαη gяυρ ιηι υηтυк мємυтαя мυѕιк ∂ι ν¢g"
                    )
                    await lel.edit(
                        "<b>✅ нєℓρєя υѕєявσт вєяgαвυηg ∂єηgαη σвяσℓαη gяσυρѕ αη∂α</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 кєѕαℓαнαη тυηggυ ∂υℓυ кηтℓ 🔴 \nUser {user.first_name} тι∂αк ∂αραт вєяgαвυηg ∂єηgαη gяυρ αη∂α кαяєηα вαηуαкηуα ρєямιηтααη υηтυк υѕєявσт! ραѕтιкαη ρєηggυηα тι∂αк ∂ιвαη ∂ι gяυρ."
                        "\n\nOr тαмвαнкαη αѕιѕтєη ѕє¢αяα мαηυαℓ кє gяυρ αη∂α ∂αη ¢σвα ℓαgι</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i> {user.first_name} υѕєявσт тι∂αк α∂α ∂αℓαм σвяσℓαη ιηι, мιηтα α∂мιη υηтυк мєηgιяιм /play ρєяιηтαн υηтυк ρєятαмα кαℓι αтαυ тαмвαнкαη {user.first_name} мαηυαℓℓу</i>"
        )
        return
    await lel.edit("🔎 <b>ƒιη∂ιηg ѕσηg</b>")
    message.from_user.id
    message.from_user.first_name

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    await lel.edit("🎵 <b>ρяσ¢єѕѕιηg</b>")
    ydl_opts = {"format": "bestaudio/best"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        # print(results)
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        await lel.edit("ℓαgυ тι∂αк ∂ιтємυкαη кηтℓ. ¢σвα ¢αяι ℓαgυ уαηg уαηg вєηєя ηαρα кηтℓ.")
        print(str(e))
        return
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❌ υ {DURATION_LIMIT} minutes тι∂αк ∂ιρєявσℓєнкαη вєямαιη!"
            )
            return
    except:
        pass
    dlurl = url
    dlurl = dlurl.replace("youtube", "youtubepp")
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📖 Playlist", callback_data="playlist"),
                InlineKeyboardButton("Menu ⏯ ", callback_data="menu"),
            ],
            [
                InlineKeyboardButton(text="🎬 YouTube", url=f"{url}"),
                InlineKeyboardButton(text="Download 📥", url=f"{dlurl}"),
            ],
            [InlineKeyboardButton(text="❌ Close", callback_data="cls")],
        ]
    )
    requested_by = message.from_user.first_name
    await generate_cover(requested_by, title, views, duration, thumbnail)
    file = await convert(youtube.download(url))
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.active_chats:
        position = await queues.put(chat_id, file=file)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"#⃣ ℓαgυ уαηg ℓυ мιηтα <b>queued</b> ℓαgι αηтяι ∂ι ρσѕιѕι {position}!",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            await callsmusic.set_stream(chat_id, file)
        except:
            message.reply("❌ ραηggιℓαη gяυρ тι∂αк тєянυвυηg αтαυ ѕαуα тι∂αк ∂αραт вєяgαвυηg")
            return
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="▶️ <b>Playing</b> ιηι ℓαgυ уαηg ∂ιмιηтα σℓєн {} via Youtube Music 😎".format(
                message.from_user.mention()
            ),
        )
        os.remove("final.png")
        return await lel.delete()


@Client.on_message(filters.command("splay") & filters.group & ~filters.edited)
async def jiosaavn(client: Client, message_: Message):
    global que
    if message_.chat.id in DISABLED_GROUPS:
        return
    lel = await message_.reply("🔄 <b>ρяσ¢єѕѕιηg</b>")
    administrators = await get_administrators(message_.chat)
    chid = message_.chat.id
    try:
        user = await USER.get_me()
    except:
        user.first_name = "crosmusic"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await client.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message_.from_user.id:
                if message_.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>⚠️ ιηgαтℓαн υηтυк мєηαмвαнкαη ρємвαηтυ кє ¢нαηηєℓ αη∂α</b>",
                    )
                try:
                    invitelink = await client.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>🙋‍♂️ тαмвαнкαη ѕαуα ѕєвαgαι α∂мιη gяυρ αη∂α тєяℓєвιн ∂αнυℓυ</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message_.chat.id, "☕ ѕαуα вєяgαвυηg ∂єηgαη gяυρѕ ιηι υηтυк мємυтαя мυѕιк ∂ι ν¢g"
                    )
                    await lel.edit(
                        "<b>✅ нєℓρєя υѕєявσт вєяgαвυηg ∂єηgαη σвяσℓαη gяσυρѕ αη∂α</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 кєѕαℓαнαη тυηggυ ∂υℓυ кηтℓ 🔴 \nUser {user.first_name} тι∂αк ∂αραт вєяgαвυηg ∂єηgαη gяυρ αη∂α кαяєηα вαηуαкηуα ρєямιηтααη υηтυк υѕєявσт! ραѕтιкαη ρєηggυηα тι∂αк ∂ιвαη ∂ι gяυρ."
                        "\n\nOr тαмвαнкαη αѕιѕтєη ѕє¢αяα мαηυαℓ кє gяυρ αη∂α ∂αη ¢σвα ℓαgι</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            "<i> ❌ нєℓρєя υѕєявσт тι∂αк α∂α ∂αℓαм σвяσℓαη ιηι, мιηтα α∂мιη υηтυк мєηgιяιм /play ρєяιηтαн υηтυк ρєятαмα кαℓιηуα αтαυ тαмвαнкαη αѕιѕтєη ѕє¢αяα мαηυαℓ</i>"
        )
        return
    requested_by = message_.from_user.first_name
    chat_id = message_.chat.id
    text = message_.text.split(" ", 1)
    query = text[1]
    res = lel
    await res.edit(f"ѕєαя¢нιηg 🔍 for `{query}` on jio saavn")
    try:
        songs = await arq.saavn(query)
        if not songs.ok:
            await message_.reply_text(songs.result)
            return
        sname = songs.result[0].song
        slink = songs.result[0].media_url
        ssingers = songs.result[0].singers
        sthumb = songs.result[0].image
        sduration = int(songs.result[0].duration)
    except Exception as e:
        await res.edit("тι∂αк мєηємυкαη αρα-αρα!, αη∂α нαяυѕ мєηgєяʝαкαη вαнαѕα ιηggяιѕ αη∂α.")
        print(str(e))
        return
    try:
        duuration = round(sduration / 60)
        if duuration > DURATION_LIMIT:
            await cb.message.edit(
                f"❌ мυѕιк ℓєвιн ℓαмα ∂αяι {DURATION_LIMIT}min тι∂αк ∂ιρєявσℓєнкαη вєямαιη"
            )
            return
    except:
        pass
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📖 Playlist", callback_data="playlist"),
                InlineKeyboardButton("Menu ⏯ ", callback_data="menu"),
            ],
            [
                InlineKeyboardButton(
                    text="🌻 υρ∂αтєѕ ¢нαηηєℓ", url=f"https://t.me/{updateschannel}"
                )
            ],
            [InlineKeyboardButton(text="❌ Close", callback_data="cls")],
        ]
    )
    file = await convert(wget.download(slink))
    chat_id = get_chat_id(message_.chat)
    if chat_id in callsmusic.active_chats:
        position = await queues.put(chat_id, file=file)
        qeue = que.get(chat_id)
        s_name = sname
        r_by = message_.from_user
        loc = file
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await res.delete()
        m = await client.send_photo(
            chat_id=message_.chat.id,
            reply_markup=keyboard,
            photo="final.png",
            caption=f"✯{bn}✯=#️⃣ αηтяι ∂ι ρσѕιѕι {position}",
        )

    else:
        await res.edit_text(f"{bn}=▶️ Playing.....")
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = sname
        r_by = message_.from_user
        loc = file
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            await callsmusic.set_stream(chat_id, file)
        except:
            res.edit("❌ ραηggιℓαη gяυρ тι∂αк тєянυвυηg кαяєηα ѕαуα тι∂αк ∂αραт вєяgαвυηg")
            return
    await res.edit("Generating Thumbnail.")
    await generate_cover(requested_by, sname, ssingers, sduration, sthumb)
    await res.delete()
    m = await client.send_photo(
        chat_id=message_.chat.id,
        reply_markup=keyboard,
        photo="final.png",
        caption=f"Playing {sname} Via Jiosaavn",
    )
    os.remove("final.png")


@Client.on_callback_query(filters.regex(pattern=r"plll"))
async def lol_cb(b, cb):
    global que

    cbd = cb.data.strip()
    chat_id = cb.message.chat.id
    typed_ = cbd.split(None, 1)[1]
    # useer_id = cb.message.reply_to_message.from_user.id
    try:
        x, query, useer_id = typed_.split("|")
    except:
        await cb.message.edit("ℓαgυ тι∂αк ∂ιтємυкαη")
        return
    useer_id = int(useer_id)
    if cb.from_user.id != useer_id:
        await cb.answer(
            "αη∂α вυкαη σяαηg уαηg мємιηтα υηтυк мємυтαя ℓαgυ!", show_alert=True
        )
        return
    await cb.message.edit("🔁 **мємρяσѕєѕ, кαℓσ ∂єℓαу ѕαвαя кσηтσℓ")
    x = int(x)
    try:
        useer_name = cb.message.reply_to_message.from_user.first_name
    except:
        useer_name = cb.message.from_user.first_name

    results = YoutubeSearch(query, max_results=5).to_dict()
    resultss = results[x]["url_suffix"]
    title = results[x]["title"][:40]
    thumbnail = results[x]["thumbnails"][0]
    duration = results[x]["duration"]
    views = results[x]["views"]
    url = f"https://youtube.com{resultss}"

    try:
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        if (dur / 60) > DURATION_LIMIT:
            await cb.message.edit(
                f"❌ мυѕιк ℓєвιн ℓαмα ∂αяι {DURATION_LIMIT}min тι∂αк ∂ιρєявσℓєнкαη вєямαιη"
            )
            return
    except:
        pass
    try:
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    except Exception as e:
        print(e)
        return
    dlurl = url
    dlurl = dlurl.replace("youtube", "youtubepp")
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📖 Playlist", callback_data="playlist"),
                InlineKeyboardButton("Menu ⏯ ", callback_data="menu"),
            ],
            [
                InlineKeyboardButton(text="🎬 YouTube", url=f"{url}"),
                InlineKeyboardButton(text="Download 📥", url=f"{dlurl}"),
            ],
            [InlineKeyboardButton(text="❌ Close", callback_data="cls")],
        ]
    )
    requested_by = useer_name
    await generate_cover(requested_by, title, views, duration, thumbnail)
    file = await convert(youtube.download(url))
    if chat_id in callsmusic.active_chats:
        position = await queues.put(chat_id, file=file)
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await cb.message.delete()
        await b.send_photo(
            chat_id,
            photo="final.png",
            caption=f"#⃣  ℓαgυ уαηg ∂ιмιηтα σℓєн {r_by.mention()} <b>queued</b> ℓαgι αηтяι ∂ι ρσѕιѕι {position}!",
            reply_markup=keyboard,
        )
        os.remove("final.png")

    else:
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)

        await callsmusic.set_stream(chat_id, file)
        await cb.message.delete()
        await b.send_photo(
            chat_id,
            photo="final.png",
            reply_markup=keyboard,
            caption=f"▶️ <b>Playing</b> ιηι ℓαgυ уαηg ∂ιмιηтα σℓєн {r_by.mention()} via Youtube Music 😎",
        )
        os.remove("final.png")
