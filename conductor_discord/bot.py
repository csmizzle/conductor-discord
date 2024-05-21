"""
Get all historical messages from a channel
"""
from conductor_discord.models import InternalKnowledgeChat
from conductor_discord.utils import (
    send_marketing_crew_request,
    upload_dict_to_s3,
    search as search_,
)
from conductor_discord.settings import settings
import discord
from discord import app_commands
import os
import uuid
import logging


logger = logging.getLogger("discord")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client=client)


@client.event
async def on_ready():
    for guild in client.guilds:
        print("Syncing guild:", guild.id)
        await tree.sync(guild=discord.Object(id=guild.id))
    logger.info(f"We have logged in as {client.user}")


@tree.command(
    name="collect",
    description="Collect all messages from a channel",
    guild=discord.Object(id=settings.guild_id),
)
async def collect(interaction: discord.Interaction, channel_id: str):
    await interaction.response.defer()
    collect_id = uuid.uuid4()
    messages = []
    channel = client.get_channel(int(channel_id))
    job_id = str(channel_id) + "/" + str(collect_id)
    logger.info(f"Starting collect job {job_id}")
    async for message in channel.history(limit=None):
        messages.append(
            InternalKnowledgeChat(
                source="discord",
                id=str(message.id),
                message=message.content,
                author=message.author.name,
                created_at=str(message.created_at),
                channel=message.channel.name,
            )
        )
    logger.info(f"Collected {len(messages)} messages from channel {channel_id}")
    logger.info(
        f"Uploading to S3: {os.getenv('DISCORD_S3_BUCKET')} with collect ID: {job_id}"
    )
    upload_dict_to_s3(
        data=[message.dict() for message in messages],
        bucket=os.getenv("DISCORD_S3_BUCKET"),
        key=f"{job_id}.json",
    )
    logger.info(
        f"Uploaded to S3: {os.getenv('DISCORD_S3_BUCKET')} with collect ID: {job_id}"
    )
    await interaction.followup.send(
        f"Collected {len(messages)} messages from channel {channel_id} with collect ID: {job_id}"
    )


@tree.command(
    name="research",
    description="Issue a research task to the market research crew",
    guild=discord.Object(id=settings.guild_id),
)
async def research(interaction: discord.Interaction, task: str):
    await interaction.response.defer()
    results = send_marketing_crew_request(task)
    await interaction.followup.send(results)


@tree.command(
    name="search",
    description="Search against collected messages and knowledge base",
    guild=discord.Object(id=settings.guild_id),
)
async def search(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    results = search_(query)
    await interaction.followup.send(results)
