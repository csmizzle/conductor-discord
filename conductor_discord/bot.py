"""
PyCord Evrim Bot
"""
import discord
import os
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and ready to roll!")


@bot.slash_command(name="hello", description="Say hello to the bot!")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hello!")


@bot.slash_command(name="research", description="Get the bot's latency!")
async def research(ctx: discord.ApplicationContext, url: str):
    message = await ctx.send(f"Researching {url}...")
    thread_name = f"{url} Research Thread"
    thread = await message.create_thread(name=thread_name, auto_archive_duration=60)
    print("Thread ID:", thread.id)
    await ctx.respond(f"The team has started working! Check {thread_name} for updates!")


bot.run(os.getenv("DISCORD_TOKEN"))
