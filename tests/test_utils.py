from conductor_discord.utils import send_url_marketing_request
import os

TEST_THREAD_ID = os.getenv("TEST_THREAD")


def test_send_url_marketing_request_key_questions():
    response = send_url_marketing_request(
        company_url="https://trssllc.com",
        thread_id=TEST_THREAD_ID,
        style="NARRATIVE",
        key_questions=[
            "What is the company's mission statement?",
            "Who are the primary competitors?",
        ],
    )
    assert response.ok
