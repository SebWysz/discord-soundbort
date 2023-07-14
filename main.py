from discord.ext import commands
import discord
import random
import asyncio
import youtube_dl

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.videos = [
  'https://www.youtube.com/watch?v=XmoKM4RunZQ',
  'https://www.youtube.com/watch?v=qTmjKpl2Jk0',
  'https://www.youtube.com/watch?v=hY7m5jjJ9mM'
]
bot.soundboard = []
bot.queue = []

@bot.command(help="Says hello to you")
async def hello(ctx):
  await ctx.send("Hello, " + ctx.author.display_name + "!")


@bot.command(help="Sends a random cat video")
async def cat(ctx):
  await ctx.send(random.choice(bot.videos))


@bot.command(help="!add <name> <link> -Adds a soundboard entry with the name and link")
async def add(ctx, name: str, link: str):
  for entry in bot.soundboard:
    if entry[0] == name.lower():
      await ctx.send("Existing entry has this name, please choose a different name.")
      return
  await ctx.send("Adding to soundboard!")
  bot.soundboard.append([name.lower(), link])


@bot.command(help="!play <name> -Plays the soundboard entry with the given name") 
async def play(ctx, name: str):
    if ctx.author.voice == None or ctx.author.voice.channel == None:
        await ctx.send("Please connect to a voice channel to use this command.")
        return
    if len(bot.soundboard) == 0:
        await ctx.send("Add something to the soundboard first using !add <name> <link>")
        return
    if bot.voice_clients:
        vc = bot.voice_clients[0]
    else:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
    bot.queue.append(name)
    if vc.is_playing():
        await ctx.send("Already playing audio, queueing this entry.")
        return 
    while len(bot.queue) > 0:
        name = bot.queue.pop(0)
        valid_entry = False
        for entry in bot.soundboard:
            if entry[0] == name:
                valid_entry = True
                await ctx.send("Playing " + entry[0])
                ydl_opts = {'format': 'bestaudio'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(entry[1], download=False)
                    URL = info['formats'][0]['url']
                    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=URL))
                    while vc.is_playing():
                        await asyncio.sleep(.1)
    if not valid_entry:
        await ctx.send("No entry with that name. !help for a list of commands and how to use them.")
    await vc.disconnect()

@bot.command(help="Stops the bot from playing audio")
async def stop(ctx):
    await ctx.send("Stopping")
    vc = ctx.author.voice.channel
    await vc.disconnect()

@bot.command(help="Lists all the soundboard entries")
async def list(ctx):
    await ctx.send("Here is the list of soundboard entries:")
    for entry in bot.soundboard:
        await ctx.send(entry[0])

@bot.command(name="remove", aliases=["delete", "del", "rm"], help="Removes a soundboard entry with the given name")
async def remove(ctx, name: str):
    for entry in bot.soundboard:
        if entry[0] == name:
            bot.queue.remove(entry[0])
            await ctx.send("Removed " + name)
            return
    await ctx.send("No entry with that name. !help for a list of commands and how to use them.")

@bot.command(name="queue", aliases=["q"], help="Shows the queue.")
async def queue(ctx):
    if len(bot.queue) == 0:
        await ctx.send("The queue is empty.")
        return
    await ctx.send("Here is the queue:")
    for name in bot.queue:
        await ctx.send(name)

from decouple import config
BOT_TOKEN = config('BOT_TOKEN')
bot.run(BOT_TOKEN)
