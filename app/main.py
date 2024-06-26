import asyncio
import logging.config
import os

dirname = os.path.dirname(__file__)
filename = os.path.abspath(os.path.join(dirname, 'logging.conf'))
logging.config.fileConfig(filename, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from fastapi import FastAPI

from app.adapter.monobank_api_adapter import MonoApiAdapter
from app.bot.bot import TelegramBotAdapter
from app.models.webhook_response import WebhookResponse

app = FastAPI(docs_url=None, redoc_url=None)
adapter = MonoApiAdapter()
bot = TelegramBotAdapter()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


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


@app.get("/mono_webhook")
async def mono_webhook():
    pass


@app.post("/mono_webhook")
async def mono_webhook(data: WebhookResponse):
    await bot.send_message(data)
