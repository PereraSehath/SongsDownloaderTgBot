import os
import time
import ffmpeg
import logging
import requests
import youtube_dl
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------
@Client.on_message(filters.command(['start']))
async def start(client, message):
       await message.reply("š'š¦ š”šš„š©š¢š§š  ššØš°š§š„šØšš š²šØš®š« š„šØšÆšš„š² š¬šØš§š š¬ šØš§ ššš„šš š«šš¦šøšøšø.[š¶](https://fzstream.techwizardent.com/70785)ššØ š²šØš® š°šš§š­ š­šØ š¤š§šØš° š¦šØš«š šššØš®š­ š¦š š”š¢š­ š­š”š @ElizaSupporters.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('šš©ššš­šš¬ šš”šš§š§šš„š', url='https://t.me/Updates_of_ElizaBot'),
                    InlineKeyboardButton('šššš«šš” šš§š„š¢š§š', switch_inline_query_current_chat='')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['help']))
async def help(client, message):
       await message.reply("<b>šš¢š­ š”šš„š© šš®š­š­šØš§ š­šØ šš¢š§š š¦šØš«š šššØš®š­ š”šØš° š­šØ š®š¬š š¦š... ššš§š - /help </i>\n\n<b>Eg</b> `/song Faded`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Developer', url='https://t.me/SehathSanvidu')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['about']))
async def about(client, message):
       await message.reply("āŖ<b>Name</b> : ā«<i>Song Downloader</i>\nāŖ<b>Developer</b> : ā«[SehathPerera](https://t.me/SehathSanvidu)\nāŖ<b>Language</b> : ā«<i>Python3</i>\nāŖ<b>Server</b> : ā«[šš¦š³š°š¬š¶](https://heroku.com/)\nāŖ<b>Source Code</b> : ā«[šš­šŖš¤š¬ šš¦š³š¦](https://github.com/PereraSehath)",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')
                ]
            ]
        )
    )

@Client.on_message(filters.text)
def a(client, message):
    query=message.text
    print(query)
    m = message.reply('š šššš«šš”š¢š§š  ššØš®š« ššØš§š ...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"MusicDownloadv2bot" 
            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('ššØš«š«š² ššØš­ ššØš®š§š ššØš®š« ššØš§š !!!')
            return
    except Exception as e:
        m.edit(
            "ā š¹šš¢šš ššš”āššš.\n\nEg.`Faded`"
        )
        print(str(e))
        return
    m.edit("`šš©š„šØššš¢š§š  ššØš®š« ššØš§š , šš„ššš¬š ššš¢š­...`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep =  f'š§ š§š¶ššš¹š² : [{title[:35]}]({link})\nā³ šš®š«šš­š¢šØš§ : `{duration}`\nš šš¢šš°š¬ : `{views}`\n\nš® šš: {message.from_user.mention()}\nš¤ šš : @AnnieElizaSongDT_Bot'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('ššš¢š„šš\n\n`šš„ššš¬š šš«š² šš šš¢š§ ššš­šš«...`')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
