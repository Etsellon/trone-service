from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WalletRequestBase(BaseModel):
    wallet_address: str
    balance: float
    total_free_bandwidth: int
    energy: int


class WalletRequestCreate(WalletRequestBase):
    pass


class WalletRequestResponse(WalletRequestBase):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
