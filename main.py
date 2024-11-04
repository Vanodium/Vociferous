from secret_token import TOKEN
from config import *
import sqlite3

import youtube_dl
import discord
from discord.utils import get


class VociferousClient(discord.Client):
    async def on_ready(self):
        await client.change_presence(activity = discord.Game("bot by https://github.com/Vanodium"))
        for guild in self.guilds:
            print(f'{self.user} connected to chat:{guild.name}(id: {guild.id})')
        await self.join_voice(bot_voicechannel_id)

    async def join_voice(self, channel_id):
        voice_channel = client.get_channel(channel_id)
        await voice_channel.connect()

    async def on_message(self, message):
        msg = message.content.lower()
        if message.channel.id == bot_txtchannel_id:
            if '!stream' in msg:
                radio = VociferousRadioPlayer()
                if 'https://www.youtube.com/watch' in msg:
                    link = msg.split()[1]
                    await radio.youtube_radio(link)
                else:
                    await radio.choose_genre(message)
            elif '!play' in msg:
                YT_videoplayer = VociferousYTPlayer()
                await YT_videoplayer.youtube_audio(message)
            elif '!pause' in msg:
                YT_videoplayer = VociferousYTPlayer()
                await YT_videoplayer.pause_song(message)
            elif '!resume' in msg:
                YT_videoplayer = VociferousYTPlayer()
                await YT_videoplayer.resume_song(message)
            elif '!role' in msg:
                if 'remove' in msg:
                    await self.change_role(message, 'remove')
                else:    
                    await self.change_role(message, 'add')
            elif '!faq' in msg:
                await message.channel.send(en_user_messages.more_info())
            elif '!help' in msg:
                await message.channel.send(embed=en_user_messages.help(True))
            else:
                if message.author != client.user:
                    await message.channel.send(embed=en_user_messages.help(False))

    async def change_role(self, message, action):
        try:
            user = message.author
            role_name = message.content.split()[1]
            role = discord.utils.get(message.guild.roles, name=role_name)
            if role not in user.roles:
                if action == 'add':
                    await user.add_roles(role)
                    await message.channel.send(en_user_messages.give_role(role_name))
                else:
                    await user.remove_roles(role)
                    await message.channel.send(en_user_messages.remove_role(role_name))
            else:
                if action == 'add':
                    await message.channel.send(en_user_messages.already_have_role())
                else:
                    await message.channel.send(en_user_messages.wrong_remove_role())
        except:
            await message.channel.send(embed=en_user_messages.help(False))


class VociferousYTPlayer(VociferousClient, discord.Client):
    def __init__(self):
        super().__init__()
        # параметры загрузки видео
        self.ydl_opts = {
                    'outtmpl': music_folder + '/%(id)s.%(ext)s',
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'm4a',
                        'preferredquality': '96',
                    }],
                }

    async def youtube_audio(self, message):
        status_message = await message.channel.send(en_user_messages.song_preparing())
        try:
            link = [message.content.split()[1]]
        except:
            await status_message.edit(embed=en_user_messages.help(False))
        able_to_play = await self.download_song(link)
        if able_to_play:
            await self.play_song(f'{music_folder}/{link[0].split('v=')[1]}.m4a', status_message)
            await status_message.edit(content=en_user_messages.playing())
        else:
            if "www.youtube.com" in message.content:
                await status_message.edit(content=en_user_messages.downloading_error())
            else:
                await status_message.edit(embed=en_user_messages.help(False))

    async def download_song(self, link):
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download(link)
                return True
        return False

    async def play_song(self, name, status_message):
        await status_message.edit(content=en_user_messages.song_ready())
        voice = get(client.voice_clients)
        voice.pause()
        voice.play(discord.FFmpegPCMAudio(name))

    async def pause_song(self, message):
        await message.channel.send(en_user_messages.song_paused())
        voice = get(client.voice_clients)
        voice.pause()

    async def resume_song(self, message):
        await message.channel.send(en_user_messages.song_resumed())
        voice = get(client.voice_clients)
        voice.resume()


class VociferousRadioPlayer(VociferousClient, discord.Client):
    def __init__(self):
        super().__init__()
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'True'}
    
    async def choose_genre(self, message):
        status_message = await message.channel.send(en_user_messages.stream_preparing())
        genre = " ".join(message.content.lower().split()[1::])
        link = await self.get_link_by_genre(genre)
        if link:
            print(link)
            await self.youtube_radio(link, status_message)
    
    async def get_link_by_genre(self, genre):
        try:
            con = sqlite3.connect(radiostations_base)
            cur = con.cursor()
            link = cur.execute("""SELECT genre, link FROM Links_by_genres WHERE Genre = ?""", (genre,)).fetchall()[0][1]
            con.close()
            return link
        except:
            channel = client.get_channel(bot_txtchannel_id)
            await channel.send(en_user_messages.wrong_genre())
            return

    async def youtube_radio(self, link, status_message):
        voice = get(client.voice_clients)
        ydl = youtube_dl.YoutubeDL(self.YDL_OPTIONS)
        with ydl:
            info = ydl.extract_info(link, download=False)
            url = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url, **self.FFMPEG_OPTIONS)
            voice.pause()
            voice.play(source)
            await status_message.edit(content=en_user_messages.playing())


client = VociferousClient()
client.run(TOKEN)
