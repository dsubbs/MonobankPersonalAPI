from pydantic import BaseModel


class WebhookResponse(BaseModel):
    type: str
    data: dict
