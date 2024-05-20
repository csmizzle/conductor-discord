from pydantic_settings import BaseSettings
import os


class DiscordBotSettings(BaseSettings):
    discord_token: str
    conductor_url: str
    conductor_username: str
    conductor_password: str
    guild_id: int


settings = DiscordBotSettings(
    discord_token=os.getenv("DISCORD_TOKEN"),
    conductor_url=os.getenv("CONDUCTOR_URL"),
    conductor_username=os.getenv("CONDUCTOR_USERNAME"),
    conductor_password=os.getenv("CONDUCTOR_PASSWORD"),
    guild_id=int(os.getenv("GUILD_ID")),
)
