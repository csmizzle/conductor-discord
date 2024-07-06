"""
PyCord Evrim Bot
"""
import discord
from dotenv import load_dotenv
from conductor_discord.utils import send_url_marketing_request

load_dotenv()
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and ready to roll!")


@bot.slash_command(name="hello", description="Say hello to the bot!")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hello!")


@bot.slash_command(
    name="research", description="Submit a URL to kick off the market research team."
)
async def research(ctx: discord.ApplicationContext, url: str):
    message = await ctx.send(f"Researching {url}...")
    thread_name = f"{url} Research Thread"
    thread = await message.create_thread(name=thread_name, auto_archive_duration=60)
    request = send_url_marketing_request(company_url=url, thread_id=thread.id)
    if request.ok:
        await ctx.respond(
            f"The team has started working! Check {thread_name} for updates!"
        )
    else:
        await ctx.respond(
            "Something went wrong. Please try again later. @csmizzle help!"
        )
