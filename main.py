import os
import aiohttp
import discord
from discord.ext import commands
from discord_slash import SlashCommand
import random
import re
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


@commands.command()
async def join_voice(self, ctx):
    connected = ctx.author.voice
    if connected:
        await connected.channel.connect()


@bot.event
async def on_ready():
    print('bot connected')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(' гавяшки'))


@commands.has_permissions(administrator=True)
@bot.command()
async def say(ctx, *, arg):
    await ctx.channel.purge(limit=1)
    await ctx.send(arg)


@slash.slash(description="Send the details of the lobby of SiGame")
async def sigame(ctx):
    await ctx.send('Программа на пк: <https://vladimirkhil.com/si/game>\n'
                   'Онлайн: <https://vladimirkhil.com/si/online/>\n'
                   'Название лобби: яя\n'
                   'Пароль: 1099\n',
                   file=discord.File('./sigame.png'))


@slash.slash(description="Post a random picture with dog and some fact")
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
        # This time we'll get the fact request as well!
        request2 = await session.get('https://some-random-api.ml/facts/dog')
        factjson = await request2.json()

    embed = discord.Embed(title="Doggo!", color=discord.Color.purple())
    embed.set_image(url=dogjson['link'])
    embed.set_footer(text=factjson['fact'])
    await ctx.send(embeds=[embed])


@slash.slash(description="Wink with a random wink-GIF ;)")
async def wink(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/animu/wink')
        winkjson = await request.json()

    embed = discord.Embed()
    embed.set_image(url=winkjson['link'])
    await ctx.send(embeds=[embed])


async def dp(ctx, *, member: discord.Member):
    userAvatar = member.avatar_url
    return(userAvatar)

def get_member(ctx, mention):
    user_id = int(re.sub('\\D', '', mention))
    users = [member for member in ctx.channel.members if member.id == user_id]
    if users:
        return users[0]
    return None




@slash.slash(description="Send a random hug GIF")
async def hug(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/animu/hug')
        hug_json = await request.json()

    embed = discord.Embed()
    embed.set_image(url=hug_json['link'])
    await ctx.send(embeds=[embed])


@slash.slash(description="Flip a coin")
async def coinflip(ctx):
    await ctx.send(random.choice(['Heads', 'Tails']))


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(973593062045548636)  # channel_id of the channel you want the message to be displayed
    await channel.send(f"{member.mention} проскальзывает на сервер! Введите текст.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() in ("да", "дa"):
        await message.channel.send(content='пизда')

    if message.content.lower() == "нет":
        await message.channel.send(content='пидора ответ')

    await bot.process_commands(message)


bot.run(token)
#garbage
@slash.slash(description="Send your super youtube comment")
async def youtube(ctx, mention, comment):
    user = get_member(ctx, mention)
    async with aiohttp.ClientSession() as session:
        query_string = urlencode({'username': user.display_name, 'comment': comment, 'avatar': user.avatar_url})
        request = await session.get(f"https://some-random-api.ml/canvas/youtube-comment?"
                                    + query_string)
    a = request.url
    await ctx.send(f"{a}")

