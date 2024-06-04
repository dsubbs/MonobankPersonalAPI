import logging
import os
import requests
from dotenv import load_dotenv

from app.models.account_info import AccountInfo

load_dotenv()


class MonoApiAdapter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @property
    def token(self) -> str:
        return os.getenv("MONOBANK_API_KEY")

    @property
    def webhook_url(self):
        return os.getenv("MONOBANK_WEBHOOK_URL")

    @property
    def receiver_url(self):
        return os.getenv("MONOBANK_RECEIVER_URL")

    @property
    def account_info_url(self):
        return os.getenv("MONOBANK_ACCOUNT_INFO_URL")

    async def set_webhook(self):
        self.logger.info(f"Setting webhook url",
                         extra={
                             "webhook_url": self.webhook_url,
                             "is_token": bool(self.token),
                             "receiver_url": self.receiver_url
                         })
        requests.post(url=self.webhook_url,
                      headers={"X-Token": self.token},
                      json={"webHookUrl": self.receiver_url})

    async def get_account_info(self) -> AccountInfo:
        self.logger.info(f"Getting account info",
                         extra={
                             "is_token": bool(self.token)
                         })
        response = requests.get(url=self.account_info_url,
                            headers={"X-Token": self.token}).json()

        return AccountInfo(**response)

