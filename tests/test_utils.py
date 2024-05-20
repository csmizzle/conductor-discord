"""
Test utils for the discord bot
"""
from conductor_discord.utils import send_marketing_crew_request
import os
import vcr

BASEDIR = os.path.dirname(os.path.abspath(__file__))


@vcr.use_cassette(f"{BASEDIR}/casettes/test_marketing_crew.yaml")
def test_marketing_crew_request():
    """
    Test the marketing crew request
    """
    response = send_marketing_crew_request("Tell me about CTOs in McLean, VA.")
    assert response.ok


test_marketing_crew_request()
