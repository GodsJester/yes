import json
import os
import platform
import random
import sys

import discord
from discord.ext import tasks
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext

import exceptions

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

"""	
Guide for myself:

Default Intents:
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.emojis = True
intents.bans = True
intents.guild_typing = False
intents.typing = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.guild_messages = True
intents.guild_reactions = True
intents.integrations = True
intents.invites = True
intents.voice_states = False
intents.webhooks = False

Privileged Intents (Needs to be enabled on dev page), please use them only if you need them:
intents.presences = True
intents.members = True
"""

intents = discord.Intents.default()

bot = Bot(command_prefix="", intents=intents)  
slash = SlashCommand(bot, sync_commands=True)



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()



@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["with you!", "with Krypton!", "with humans!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))



bot.remove_command("help")

if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")



@bot.event
async def on_message(message: discord.Message):
    
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)



@bot.event
async def on_slash_command(ctx: SlashContext):
    full_command_name = ctx.name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {ctx.guild.name} (ID: {ctx.guild.id}) by {ctx.author} (ID: {ctx.author.id})")



@bot.event
async def on_slash_command_error(context: SlashContext, error: Exception):
    if isinstance(error, exceptions.UserBlacklisted):
        print("A blacklisted user tried to execute a command.")
        return await context.send("You are blacklisted from using the bot.", hidden=True)
    raise error



bot.run(config["OTEwOTE4MjI4MzYzMDUxMDg5.YZZ0tQ.EWqSGIcTsKu2iD-mZQEHiHzBnq8"])
