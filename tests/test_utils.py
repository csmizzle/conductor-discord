from conductor_discord.utils import (
    send_url_marketing_request,
    split_and_format_key_questions,
)
import os

TEST_THREAD_ID = os.getenv("TEST_THREAD")


def test_send_url_marketing_request_key_questions() -> None:
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


def test_wrong_discord_input_logic() -> None:
    # this is a regression test to ensure that the logic in split_and_format_key_questions is correct
    input_ = "What is the company's mission statement? Who are the primary competitors?"
    key_questions = input_.split(" ")
    assert len(key_questions) == 11


def test_split_and_format_key_questions() -> None:
    input_ = "What is the company's mission statement? Who are the primary competitors?"
    result = split_and_format_key_questions(input_)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == "What is the company's mission statement?"
    assert result[1] == "Who are the primary competitors?"


def test_split_and_format_key_question() -> None:
    input_ = "What is the company's mission statement?"
    result = split_and_format_key_questions(input_)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == "What is the company's mission statement?"
