from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TweetIn(BaseModel):
    content: str = Field(..., alias="tweet_data")
    tweet_media_ids: list[int] | None = None


class TweetOut(BaseModel):
    result: bool
    tweet_id: int
    model_config = ConfigDict(from_attributes=True)


class AttachmentBase(BaseModel):
    link: str


class UserBase(BaseModel):
    id: int
    name: str


class LikeBase(BaseModel):
    user_id: int
    id: int


class TweetResponse(BaseModel):
    id: int
    content: str
    attachments: Optional[List[AttachmentBase]]
    author: UserBase
    likes: List[LikeBase]

    @field_validator("attachments", mode="after")
    @classmethod
    def extract_attachments(cls, values: List[AttachmentBase]) -> Optional[List[str]]:
        return [value.link for value in values]


class TweetsResponseOut(BaseModel):
    result: bool
    tweets: List[TweetResponse]
