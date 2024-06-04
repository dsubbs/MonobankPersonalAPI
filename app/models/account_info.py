from pydantic import BaseModel


class AccountInfo(BaseModel):
    clientId: str
    name: str
    webHookUrl: str
    permissions: str
    accounts: list
    jars: list
