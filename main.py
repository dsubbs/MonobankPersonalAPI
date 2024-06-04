import asyncio
import logging.config
import os

dirname = os.path.dirname(__file__)
filename = os.path.abspath(os.path.join(dirname, 'logging.conf'))
logging.config.fileConfig(filename, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from fastapi import FastAPI

from adapter.monobank_api_adapter import MonoApiAdapter
from bot.bot import TelegramBotAdapter
from models.webhook_response import WebhookResponse

app = FastAPI()
adapter = MonoApiAdapter()
bot = TelegramBotAdapter()


@app.get("/get_info")
async def get_info():
    account = await adapter.get_account_info()
    await bot.send_message(account)


@app.post("/setup_webhook")
async def setup_webhook():
    try:
        await adapter.set_webhook()
    except Exception as ex:
        logger.exception(ex)

    return


@app.post("/mono_webhook")
async def mono_webhook(data: WebhookResponse):
    await bot.send_message(data)
