"""
PyCord Evrim Bot
"""
import discord
from conductor_discord.utils import send_url_marketing_request

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
async def research(
    ctx: discord.ApplicationContext,
    url: discord.Option(
        discord.SlashCommandOptionType.string, "URL to research", required=True
    ),
    report_style: discord.Option(
        discord.SlashCommandOptionType.string,
        "Report Style",
        required=True,
        choices=["Narrative", "Bulleted"],
    ),
) -> None:
    message = await ctx.send(f"Researching {url}...")
    thread_name = f"{url} Research Thread"
    thread = await message.create_thread(name=thread_name, auto_archive_duration=60)
    request = send_url_marketing_request(
        company_url=url, thread_id=thread.id, style=report_style.upper()
    )
    if request.ok:
        await ctx.respond(
            f"The team has started working! Check {thread_name} for updates!"
        )
    else:
        await ctx.respond(
            "Something went wrong. Please try again later. <@csmizzle> help!"
        )
