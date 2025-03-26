from sqlalchemy import Text, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, uuid_pk


class TronWalletRequest(Base):
    wallet_address: Mapped[str] = mapped_column(Text, nullable=False)
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
    bandwidth: Mapped[int] = mapped_column(Integer, nullable=False)
    energy: Mapped[int] = mapped_column(Integer, nullable=False)
