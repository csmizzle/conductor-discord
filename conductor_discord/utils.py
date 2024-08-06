"""
Send request to the API
"""
import requests
from requests.models import Response
from requests.auth import HTTPBasicAuth
import os


def split_and_format_key_questions(input_: str) -> list[str]:
    split_inputs = input_.split("? ")
    for idx in range(len(split_inputs)):
        # append question mark if it was removed
        if not split_inputs[idx].endswith("?"):
            split_inputs[idx] += "?"
    return split_inputs


def send_url_marketing_request(
    company_url: str,
    thread_id: str,
    style: str,
    key_questions: list[str] = None,
) -> Response:
    endpoint = os.getenv("CONDUCTOR_URL") + "/api/v0/marketing/report/"
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


def send_url_marketing_rag_request(
    company_url: str,
    title: str,
    description: str,
    thread_id: str,
    style: str,
    tone: str,
    point_of_view: str,
) -> Response:
    """
    Sends a request to the marketing RAG (Red, Amber, Green) system for a URL.

    Args:
        company_url (str): The URL of the company.
        title (str): The title of the request.
        description (str): The description of the request.
        thread_id (str): The ID of the thread associated with the request.
        style (str): The style of the request.
        tone (str): The tone of the request.
        point_of_view (str): The point of view of the request.

    Returns:
        Response: The response from the marketing RAG system.
    """
    endpoint = os.getenv("CONDUCTOR_URL") + "/api/v1/discord/marketing/report/"
    return requests.post(
        url=endpoint,
        json={
            "url": company_url,
            "title": title,
            "description": description,
            "thread_id": thread_id,
            "proxy": False,
            "cache": True,
            "style": style,
            "tone": tone,
            "point_of_view": point_of_view,
        },
        auth=HTTPBasicAuth(
            os.getenv("CONDUCTOR_USERNAME"), os.getenv("CONDUCTOR_PASSWORD")
        ),
    )
