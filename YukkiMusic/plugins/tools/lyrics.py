#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import random
import re
import string

import lyricsgenius as lg
from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from config import BANNED_USERS, lyrical
from strings import get_command
from YukkiMusic import app
from YukkiMusic.utils.decorators.language import language

###Commands
LYRICS_COMMAND = get_command("LYRICS_COMMAND")

api_key = "82Jw_9BUVckdXKvbQlMAjietlT7IH3lqWt9cEl6iMm81z8OUmGhZ-LfLRE4UwR70"
y = lg.Genius(api_key)
y.verbose = False


@app.on_message(
    filters.command(LYRICS_COMMAND) & ~filters.edited & ~BANNED_USERS
)
@language
async def lrsearch(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(_["lyrics_1"])
    title = message.text.split(None, 1)[1]
    m = await message.reply_text(_["lyrics_2"])
    S = y.search_song(title, get_full_info=False)
    if S is None:
        return await m.edit(_["lyrics_3"].format(title))
    ran_hash = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )
    lyric = S.lyrics
    if "Embed" in lyric:
        lyric = re.sub(r"\d*Embed", "", lyric)
    lyrical[ran_hash] = lyric
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["L_B_1"],
                    url=f"https://t.me/{app.username}?start=lyrics_{ran_hash}",
                ),
            ]
        ]
    )
    await m.edit(_["lyrics_4"], reply_markup=upl)
