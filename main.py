from discord.ext import commands
import discord
import os
import random
import pafy
import time
from discord import FFmpegPCMAudio, PCMVolumeTransformer

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.videos = [
  'https://www.youtube.com/watch?v=XmoKM4RunZQ',
  'https://www.youtube.com/watch?v=qTmjKpl2Jk0',
  'https://www.youtube.com/watch?v=hY7m5jjJ9mM'
]
bot.happylist = []
bot.soundboard = []


@bot.command()
async def hello(ctx):
  await ctx.send("Hello, " + ctx.author.display_name + "!")


@bot.command()
async def cat(ctx):
  await ctx.send(random.choice(bot.videos))


@bot.command()
async def happy(ctx, *, item):
  await ctx.send("Awesome!")
  bot.happylist.append(item)
  print(bot.happylist)


@bot.command()
async def sad(ctx):
  await ctx.send("Hope this makes you feel better")
  await ctx.send(random.choice(bot.happylist))


@bot.command()
async def calc(ctx, x: float, fn: str, y: float):
  if fn == '+':
    await ctx.send(x + y)
  elif fn == '-':
    await ctx.send(x - y)
  elif fn == '*':
    await ctx.send(x * y)
  elif fn == '/':
    await ctx.send(x / y)
  else:
    await ctx.send("We only support 4 function operations")


@bot.command()
async def add(ctx, name: str, link: str):
  for entry in bot.soundboard:
    if entry[0] == name.lower():
      await ctx.send("Existing entry has this name, please choose a different name.")
      return
  await ctx.send("Adding to soundboard!")
  bot.soundboard.append([name.lower(), link])


@bot.command() 
async def play(ctx, name: str):
  if ctx.author.voice == None or ctx.author.voice.channel == None:
    await ctx.send("Please connect to a voice channel to use this command.")
    return
  if len(bot.soundboard) == 0:
    await ctx.send("Add something to the soundboard first!")
    return

  valid_entry = False
  for entry in bot.soundboard:
    if entry[0] == name:
      await ctx.send("Playing " + entry[0])
      voice_channel = ctx.author.voice.channel
      channel = voice_channel.name
      song = pafy.new(entry[1])
      audio = song.getbestaudio()
      source = FFmpegPCMAudio(entry[1], **FFMPEG_OPTIONS)
      vc = await voice_channel.connect()
      vc.play(source)
      while vc.is_playing():
        time.sleep(.1)
      await vc.disconnect()
      valid_entry = True
  if not valid_entry:
    await ctx.send("No entry with that name")


TOKEN = os.environ['password']
bot.run(TOKEN)

#what next?
#add a stop command
#add a list command
#add a remove command
#add a help command
#add a queue command
#add a skip command