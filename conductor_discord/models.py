from pydantic import BaseModel


class InternalKnowledgeChat(BaseModel):
    id: str
    message: str
    author: str
    created_at: str
    source: str
    channel: str
