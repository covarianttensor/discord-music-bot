import asyncio
import requests
from rich import print
import nextcord
from nextcord.ext import commands, tasks
from helpers.youtube import get_audio_info, get_audio_search_results, get_query_type
from lib.base_cog import BaseCog
from lib.music_classes import MusicTrack
from typing import Union, Dict, List
from configs.constants import ADMIN_ROLE_NAME

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

class Music(BaseCog):
    """
    This cog plays music from YouTube.
    """
    def __init__(self, bot):
        super().__init__(bot)
        self.ctx: Union[commands.Context,None] = None
        self.voice_client: Union[nextcord.VoiceClient,None] = None
        self.play_next = asyncio.Event()
        self.queue = []
        self.current_track = MusicTrack()
        self.is_first_song = True

    #==========================================================
    #=====================Helper Methods=======================
    #==========================================================

    async def join_voice(self,ctx: commands.Context):
        """
        Returns true if bot is in or joins author's voice channel.
        """
        # Check if author is in a voice chat
        if ctx.author.voice is None:
            await self.send_error_embed(ctx,"Voice Client Error",
                "You\'re not in voice channel. How the fuck am I supposed to play you music? Try again once you\'re in one of those")
            return False

        # Check if voice client is set
        if self.voice_client is None:
            # Bot is not connected to any voice channel
            if ctx.voice_client is None:
                # Connect to author's voice channel
                await ctx.author.voice.channel.connect()
                # Initialize our class voice client
                self.voice_client = ctx.voice_client
                self.is_first_song = True
        elif self.voice_client.channel != ctx.author.voice.channel:
            # Move to author's voice chat if different from ours
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            # Initialize our class voice client
            self.voice_client = ctx.voice_client
            self.is_first_song = True

        # Update context everytime
        self.ctx = ctx
        return True

    async def send_track_embed(self, ctx: commands.Context, text:str, color:int,queued_track=None):
        track = self.current_track
        if queued_track:
            track = queued_track
        normal_desc=f'**Track:** *{track.title}*\n**Duration:** *{track.duration}*\n**Added by:** {track.added_by}'
        queue_desc=f"**Track:** *{track.title}*\n**Duration:** *{track.duration}*\n**Queue Position:** *#{len(self.queue)+1}*\n**Added by:** {track.added_by}"
        desc=normal_desc
        if queued_track:
            desc=queue_desc
        embed = nextcord.Embed(
            title=text,
            description=desc,
            color = color)
        embed.set_thumbnail(url=track.source_thumb_url)
        embed.set_author(name=track.source, url=track.webpage_url, icon_url=track.source_icon_url)
        await ctx.send(embed=embed)

    async def send_error_embed(self, ctx: commands.Context, error_type:str, message:str):
        embed = nextcord.Embed(
            title=f"{error_type} ❌",
            description=f'```{message}```',
            color = 0xFF0000)
        await ctx.send(embed=embed)

    #==========================================================
    #=========================EVENTS===========================
    #==========================================================

    #==========================================================
    #========================TASKS=============================
    #==========================================================

    @tasks.loop(count=1)
    async def music_queue(self):
        while True:
            # Blocking call until event is set
            await self.play_next.wait()
            self.play_next.clear() # Clear event
            
            # Proceeed with queue
            if len(self.queue) <= 0:
                # Queue is empty
                break # End task

            # Dequeue next song
            self.current_track = self.queue.pop(0)
            
            # Play the song
            source = await nextcord.FFmpegOpusAudio.from_probe(self.current_track.stream_url, **FFMPEG_OPTIONS)
            if self.voice_client:
                self.voice_client.play(source, after=lambda e: self.play_next.set()) # will fire event after playback
                # Let the user know we are playing the next song.
                if self.ctx:
                    await self.send_track_embed(self.ctx,f'Now Playing ▶️',0x00FF00)
            else:
                # Let the user know we can not play the next song.
                if self.ctx:
                    await self.send_error_embed(ctx,"Voice Client Error",
                        "Can not play next song, voice client is null. Ending queue.")
                break # End Task

    @music_queue.after_loop
    async def after_music_queue(self):
        # Clear current track info & Reset Queue
        self.current_track = MusicTrack()
        self.is_first_song = True
        self.queue = [] # clear queue
        
        # Clear blocking player event
        self.play_next.clear()

        # Let user know queue is empty.
        if self.ctx:
            await self.ctx.send(embed=nextcord.Embed(title='Music queue is empty',color = 0xFF0000))

        # Exit voice chat
        if self.voice_client is not None:
            await self.voice_client.disconnect()
        self.voice_client = None

    #==========================================================
    #=======================COMMANDS===========================
    #==========================================================

    @commands.command(name='currentsong')
    async def current_song(self,ctx):
        await self.send_track_embed(ctx, 'Current Song ▶️',0x0000FF)

    @commands.command()
    async def skip(self,ctx):
        if self.voice_client is not None:
            self.voice_client.stop()
        await self.send_track_embed(ctx, 'Skipped ⏭️',0xFF0000)

    @commands.command()
    async def pause(self,ctx):
        if self.voice_client is not None:
            self.voice_client.pause()
        await self.send_track_embed(ctx, 'Paused ⏸', 0xFFFF00)

    @commands.command()
    async def resume(self,ctx):
        # Resume
        if self.voice_client is not None:
            self.voice_client.resume()
            await self.send_track_embed(ctx, 'Resumed ⏯️',0x0000FF)
            return

        # Restart song after fixing null voice client
        if self.current_track.stream_url:
            # Rejoin VC
            if not await self.join_voice(ctx):
                return
            # Reset play event
            self.play_next.clear()
            # Start queue if necessary
            if not self.music_queue.is_running():
                self.music_queue.start()
            # Play the song
            source = await nextcord.FFmpegOpusAudio.from_probe(self.current_track.stream_url, **FFMPEG_OPTIONS)
            if self.voice_client:
                self.voice_client.play(
                    source, after=lambda e: self.play_next.set()) # will fire event after playback
                # Let the user know we are playing the current song.
                await self.send_track_embed(ctx,f'Now Playing ▶️',0x00FF00)
            return

        # Can't resume, skip to next song instead
        # Attempt to join VC
        if not await self.join_voice(ctx):
            return
        # Reset play event
        self.play_next.clear()
        # Start queue if necessary
        if not self.music_queue.is_running():
            self.music_queue.start()
        # Play the next song instead
        self.play_next.set()
    
    @commands.command()
    async def play(self,ctx: commands.Context, *, args=None,**kwargs):
        # Attempt to join VC
        if not await self.join_voice(ctx):
            return
        
        # Query YouTube
        query = str(args)
        query_type = get_query_type(query)
        info = None
        if query_type == "non_youtube_url":
            await self.send_error_embed(ctx,"Queue Error","Not a YouTube link.")
            return
        if query_type == "youtube_url":
            await ctx.send(embed=nextcord.Embed(title='Grabbing YouTube link... 🔗',color = 0xffb247))
            result = await get_audio_info(query)
            if not result['success']:
                await self.send_error_embed(ctx,"Queue Error",result["error"])
                return
            info = result['info']
        if query_type == "youtube_search":
            await ctx.send(embed=nextcord.Embed(title='Searching YouTube... 🔎',color = 0xffb247))
            result = await get_audio_search_results(query)
            if not result['success']:
                await self.send_error_embed(ctx,"Queue Error",result["error"])
                return
            info = result['search_results']['entries'][0] # Get top search result

        # Queue Song
        track = MusicTrack()
        track.set_youtube_source(ctx.author.mention,info)
        if not track.stream_url:
            await self.send_error_embed(ctx,"Queue Error","Could not find audio file to playback for video.")
            return
        self.queue.append(track)

        # Let the user know their song has been queued.
        await self.send_track_embed(ctx, 'Song Queued ✅',0xBF40BF,queued_track=track)

        # Start queue if necessary
        if not self.music_queue.is_running():
            self.music_queue.start()

        # Allow queue to play the first song.
        if self.is_first_song:
            self.is_first_song = False
            self.play_next.set()

    @commands.command(name='queue')
    async def get_queue(self,ctx):
        if len(self.queue) <= 0:
            await ctx.send(embed=nextcord.Embed(title='Music queue is empty',color = 0xFF0000))
            return
        queueStr = ''
        qpos = 1
        for track in self.queue:
            queueStr += f'**#{qpos}:** *{track.title}*\n'
            qpos += 1
        await ctx.send(embed=nextcord.Embed(title=f'Current Queue 🔢',description=queueStr,color = 0xBF40BF))

    @commands.command(name='clear')
    async def clear_queue(self,ctx):
        if len(self.queue) <= 0:
            await ctx.send(embed=nextcord.Embed(title='Music queue is already empty',color = 0xFF0000))
            return
        self.queue = []
        await ctx.send(embed=nextcord.Embed(title='Music queue has beem cleared',color = 0xFF0000))

# === Module Method(s) ===
def setup(bot):
    """
    A module method to add this module's cog to a discord bot.
    To be used by a factory module.
    """
    bot.add_cog(Music(bot))