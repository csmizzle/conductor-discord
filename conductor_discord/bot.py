"""
PyCord Evrim Bot
"""
import discord
from conductor_discord.utils import (
    send_url_marketing_request,
    split_and_format_key_questions,
    send_url_marketing_rag_request,
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
        default=None,
    ),  # type: ignore
) -> None:
    # append https:// if not included
    if not url.startswith("https://"):
        url = f"https://{url}"
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


@bot.slash_command(
    name="research_v2", description="Submit a URL to kick off the market research team."
)
async def research_v2(
    ctx: discord.ApplicationContext,
    url: discord.Option(
        discord.SlashCommandOptionType.string,
        "URL to research, try to include http:// or https://.",
        required=True,
    ),  # type: ignore
    title: discord.Option(
        discord.SlashCommandOptionType.string,
        "Title of the report",
        required=True,
    ),  # type: ignore
    description: discord.Option(
        discord.SlashCommandOptionType.string,
        "Description of the report",
        required=True,
    ),  # type: ignore
    report_style: discord.Option(
        discord.SlashCommandOptionType.string,
        "Report Style",
        required=True,
        choices=["Narrative", "Bulleted"],
    ),  # type: ignore
    report_tone: discord.Option(
        discord.SlashCommandOptionType.string,
        "Report Tone",
        required=True,
        choices=["Professional", "Informal", "Informational", "Persuasive", "Critical"],
    ),  # type: ignore
    report_pov: discord.Option(
        discord.SlashCommandOptionType.string,
        "Report Point of View",
        required=True,
        choices=["First Person", "Third Person"],
    ),  # type: ignore
) -> None:
    # append https:// if not included
    if not url.startswith("https://"):
        url = f"https://{url}"
    message = await ctx.send(f"Researching {url}...")
    thread_name = f"{url} Research Thread"
    thread = await message.create_thread(name=thread_name, auto_archive_duration=60)
    request = send_url_marketing_rag_request(
        company_url=url,
        title=title,
        description=description,
        thread_id=thread.id,
        style=report_style.upper(),
        tone=report_tone.upper(),
        point_of_view=report_pov.upper().replace(" ", "_"),
    )
    if request.ok:
        await ctx.respond(
            f"The team has started working! Check {thread_name} for updates!"
        )
    else:
        await ctx.respond(
            "Something went wrong. Please try again later. <@csmizzle> help!"
        )
