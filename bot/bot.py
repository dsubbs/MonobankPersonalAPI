import logging
import os

import telegram
from dotenv import load_dotenv

from adapter.monobank_api_adapter import MonoApiAdapter
from models.account_info import AccountInfo
from models.webhook_response import WebhookResponse

load_dotenv()


class TelegramBotAdapter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.bot = telegram.Bot(token=self.token)
        self.adapter = MonoApiAdapter()

    @property
    def token(self):
        return os.getenv("TELEGRAM_BOT_TOKEN")

    @property
    def chat_id(self):
        return os.getenv("TELEGRAM_CHAT_ID")

    async def send_message(self, data):
        if isinstance(data, WebhookResponse):
            formatting = f"Type: {data.type}; \nData: {data.data};\n"
        elif isinstance(data, AccountInfo):
            formatting = f"Name: {data.name}; \n"
            for account in data.accounts:
                account_formatting = f'Card: {account.get("maskedPan")}; Type: {account.get("type")}; Balance: {account.get("balance")}\n' if account.get("maskedPan") else ""
                formatting += account_formatting
        else:
            formatting = data
        await self.bot.send_message(chat_id=self.chat_id, text=formatting)

    async def startup(self):
        await self.bot.initialize()
        await self.bot.send_message(chat_id=self.chat_id, text="Bot started")

    async def stop(self):
        await self.bot.send_message(chat_id=self.chat_id, text="Bot stopped")
        await self.bot.shutdown()

    async def get_account_info(self):
        account = await self.adapter.get_account_info()
        await self.send_message(account)

