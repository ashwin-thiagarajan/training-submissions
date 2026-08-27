from fastapi import Request

from app.core.config import Settings
from app.services.sentiment_service import SentimentService


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_sentiment_service(request: Request) -> SentimentService:
    return request.app.state.sentiment_service

