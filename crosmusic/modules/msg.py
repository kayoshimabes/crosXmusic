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

from crosmusic.config import ASSISTANT_NAME, PROJECT_NAME


class Messages:
    START_MSG = "**ωєℓ¢σмιη 👋 [{}](tg://user?id={})!**\n\n🤖 ѕαуα вσт мυѕι¢ gяσυρ, уαηg вιѕα мємυтαя ℓαgυ ∂єηgαη ¢єραт ∂ι νσι¢є ¢нαт gяσυρ ∂єηgαη ¢αяα уαηg мυ∂αн
ѕαуα мємιℓιкι вαηуαк ƒιтυя ρяαктιѕ ѕєρєятι :
┏━━━━━━━━━━━━━━
┣• мємυтαя мυѕιк.
┣• мєη∂σωηℓσα∂ ℓαgυ.
┣• мєℓιнαт ℓιяιк ℓαgυ.
┣• мємρυηуαι вαηуαк мσ∂υℓ мєηαяιк.
┣• мєη¢αяι ℓαgυ уαηg ιηgιη ∂ι ρυтαя αтαυ di ∂σωηℓσα∂.
┣• gυηαкαη ρєяιηтαн » /help « υηтυк мєηgєтαнυι ƒιтυя ℓєηgкαρ ѕαуα
┗━━━━━━━━━━━━━━ 
❃✨тєяιмαкαѕιн тєℓαн мєηggυηαкαη ρяσʝє¢т ιηι! [GLITTER](https://t.me/{OWNER_NAME})."**
    HELP_MSG = [
        ".",
        f"""
**нαℓℓσ 👋 ωєℓ¢σмє вα¢к тσ {PROJECT_NAME}

⚪️ {PROJECT_NAME} ∂αραт мємυтαя мυѕιк ∂ι σвяσℓαη ѕυαяα gяυρ αη∂α ѕєятα σвяσℓαη ѕυαяα ѕαℓυяαη

⚪️ αѕѕιѕтαηт ηαмє >> @{ASSISTANT_NAME}\n\nкℓιк вєяιкυтηуα υηтυк ℓιαт ρєтυηʝυк**
""",
        f"""
**ѕєттιηg υρ**

1) Make bot admin (Group and in channel if use cplay)
2) Start a voice chat
3) Try /play [song name] for the first time by an admin
*) If userbot joined enjoy music, If not add @{ASSISTANT_NAME} to your group and retry

**ƒσя ¢нαηηєℓ мυѕι¢ ρℓαу**
1) Make me admin of your channel 
2) Send /userbotjoinchannel in linked group
3) Now send commands in linked group
""",
        f"""
**Commands**

**=>> ѕσηg ρℓαуιηg 🎧**

- /play: Play the requestd song
- /play [yt url] : Play the given yt url
- /play [reply yo audio]: Play replied audio
- /splay: Play song via jio saavn
- /ytplay: Directly play song via Youtube Music

**=>> ρℓαувα¢к ⏯**

- /player: Open Settings menu of player
- /skip: Skips the current track
- /pause: Pause track
- /resume: Resumes the paused track
- /end: Stops media playback
- /mute: mute song play
- /unmute: unmute song play
- /current: Shows the current Playing track
- /playlist: Shows playlist

*ρℓαуєя ¢м∂ αη∂ αℓℓ σтнєя ¢м∂ѕ єχ¢єρт /play, /current  αη∂ /playlist  αяє σηℓу ƒσя α∂мιηѕ σƒ тнє gяσυρѕ.
""",
        f"""
**=>> ¢нαηηєℓ мυѕι¢ ρℓαу 🛠**

⚪️ ƒσя ℓιηкє∂ gяσυρѕ α∂мιηѕ σηℓу:

- /cplay [song name] - play song you requested
- /csplay [song name] - play song you requested via jio saavn
- /cplaylist - Show now playing list
- /cccurrent - Show now playing
- /cplayer - open music player settings panel
- /cpause - pause song play
- /cresume - resume song play
- /cskip - play next song
- /cend - stop music play
- /cmute - mute song play
- /mute - mute song play
- /unmute - mute song play
- /userbotjoinchannel - invite assistant to your chat

¢нαηηєℓ ιѕ αℓѕσ ¢αη вє υѕє∂ ιηѕтєα∂ σƒ ¢ ( /cplay = /channelplay )

⚪️ ιƒ уσυ ∂σηℓт ℓιкє тσ ρℓαу ιη ℓιηкє∂ gяσυρѕ:

1) gєт уσυя ¢нαηηєℓ ι∂.
2) Create a group with tittle: Channel Music: your_channel_id
3) Add bot as Channel admin with full perms
4) Add @{ASSISTANT_NAME} to the channel as an admin.
5) Simply send commands in your group. (remember to use /ytplay instead /play)
""",
        f"""
**=>> мσяє тσσℓѕ 🧑‍🔧**

- /musicplayer [on/off]: Enable/Disable Music player
- /admincache: Updates admin info of your group. Try if bot isn't recognize admin
- /userbotjoin: Invite @{ASSISTANT_NAME} Userbot to your chat
""",
        f"""
**=>> ѕσηg ∂σωηℓσα∂ 🎸**

- /video [song mame]: Download video song from youtube
- /song [song name]: Download audio song from youtube
- /saavn [song name]: Download song from saavn
- /deezer [song name]: Download song from deezer

**=>> ѕєαя¢н тσσℓѕ 📄**

- /search [song name]: Search youtube for songs
- /lyrics [song name]: Get song lyrics
""",
        f"""
**=>> ¢σммαη∂ѕ ƒσя ѕυ∂σ υѕєяѕ ⚔️**

 - /userbotleaveall - remove assistant from all chats
 - /broadcast <reply to message> - globally brodcast replied message to all chats
 - /pmpermit [on/off] - enable/disable pmpermit message
*Sudo Users can execute any command in any groups

""",
    ]
