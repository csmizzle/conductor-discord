"""
PyCord Evrim Bot
"""
import discord
from conductor_discord.utils import (
    send_url_marketing_request,
    split_and_format_key_questions,
)

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and ready to roll!")


@bot.slash_command(name="hello", description="Say hello to the bot!")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond(
        "Service is up and running! Try the /research command to get started."
    )


@bot.slash_command(
    name="research", description="Submit a URL to kick off the market research team."
)
async def research(
    ctx: discord.ApplicationContext,
    url: discord.Option(
        discord.SlashCommandOptionType.string,
        "URL to research, try to include http:// or https://.",
        required=True,
    ),  # type: ignore
    report_style: discord.Option(
        discord.SlashCommandOptionType.string,
        "Report Style for output reports",
        required=True,
        choices=["Narrative", "Bulleted"],
    ),  # type: ignore
    key_questions: discord.Option(
        discord.SlashCommandOptionType.string,
        "Key Questions: questions you'd like to the team to answer. Separate each question with '? '.",
        required=False,
    ),  # type: ignore
) -> None:
    message = await ctx.send(f"Researching {url}...")
    thread_name = f"{url} Research Thread"
    thread = await message.create_thread(name=thread_name, auto_archive_duration=60)
    if key_questions:
        key_questions = split_and_format_key_questions(key_questions)
    request = send_url_marketing_request(
        company_url=url,
        thread_id=thread.id,
        style=report_style.upper(),
        key_questions=key_questions,
    )
    if request.ok:
        await ctx.respond(
            f"The team has started working! Check {thread_name} for updates!"
        )
    else:
        await ctx.respond(
            "Something went wrong. Please try again later. <@csmizzle> help!"
        )
