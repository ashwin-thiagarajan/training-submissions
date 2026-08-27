from sentiment.schemas import SentimentRequest
from sentiment.services import SentimentService


def test_sentiment_service_maps_pipeline_result() -> None:
    def fake_pipeline_factory(task: str, model: str):
        return lambda text: [{"label": "Positive", "score": 0.98}]

    service = SentimentService(pipeline_factory=fake_pipeline_factory)
    result = service.analyze(SentimentRequest(text="Great experience."))

    assert result.sentiment == "Positive"
    assert result.score == 0.98

