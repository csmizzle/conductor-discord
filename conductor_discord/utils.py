"""
Send request to the API
"""
import requests
from requests.models import Response
import os


def split_and_format_key_questions(input_: str) -> list[str]:
    split_inputs = input_.split("? ")
    for idx in range(len(split_inputs)):
        # append question mark if it was removed
        if not split_inputs[idx].endswith("?"):
            split_inputs[idx] += "?"
    return split_inputs


def get_token(
    username: str,
    password: str,
) -> dict:
    """
    Retrieves a token from the conductor server.
    Args:
        username (str): The username for authentication.
        password (str): The password for authentication.
    Returns:
        response (dict): A dictionary containing the token information.
    """
    endpoint = os.getenv("CONDUCTOR_URL") + "/token/"
    response = requests.post(
        url=endpoint, json={"username": username, "password": password}
    )
    if response.ok:
        return response.json()


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
    tokens = get_token(
        username=os.getenv("CONDUCTOR_USERNAME"),
        password=os.getenv("CONDUCTOR_PASSWORD"),
    )
    endpoint = os.getenv("CONDUCTOR_URL") + "/discord/research/"
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
        headers={"Authorization": f"Bearer {tokens['access']}"},
    )


def send_search(query: str) -> Response:
    """
    Search the vector database for the given query.

    Args:
        query (str): The search query.

    Returns:
        dict: The search response.
    """
    tokens = get_token(
        username=os.getenv("CONDUCTOR_USERNAME"),
        password=os.getenv("CONDUCTOR_PASSWORD"),
    )
    endpoint = os.getenv("CONDUCTOR_URL") + "/search/"
    return requests.post(
        url=endpoint,
        json={"search": query},
        headers={"Authorization": f"Bearer {tokens['access']}"},
    )
