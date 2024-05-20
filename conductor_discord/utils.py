"""
Send request to the API
"""
import requests
from requests.models import Response
import boto3
import json
from conductor_discord.settings import settings
from typing import Union


def upload_dict_to_s3(data: dict, bucket, key):
    """
    Uploads a dictionary to S3
    """
    s3 = boto3.client("s3")
    json_data = json.dumps(data, indent=4)
    s3.put_object(Bucket=bucket, Key=key, Body=json_data)


def send_marketing_crew_request(task: str) -> Union[Response, None]:
    """
    Sends a request to the marketing crew
    """
    response = requests.post(
        url=settings.conductor_url + "/agents/",
        auth=(settings.conductor_username, settings.conductor_password),
        json={"task": task},
    )
    if response.ok:
        return response.json()["output"]
