"""
Send request to the API
"""
import requests
from requests.models import Response
from requests.auth import HTTPBasicAuth
import os


def send_url_marketing_request(
    company_url: str,
    thread_id: str,
    style: str,
    key_questions: list[str] = None,
) -> Response:
    endpoint = os.getenv("CONDUCTOR_URL") + "/discord/marketing/report/"
    return requests.post(
        url=endpoint,
        json={
            "url": company_url,
            "thread_id": thread_id,
            "proxy": False,
            "cache": True,
            "style": style,
            "key_questions": key_questions,
        },
        auth=HTTPBasicAuth(
            os.getenv("CONDUCTOR_USERNAME"), os.getenv("CONDUCTOR_PASSWORD")
        ),
    )
