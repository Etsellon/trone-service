from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet_request import WalletRequest
from app.schemas.wallet_request import WalletRequestResponse
from app.services.tron_service import get_wallet_info
from app.services.wallet_repository import create_wallet_request, get_wallet_requests
from app.core.database import get_db

router = APIRouter()


@router.post("/wallet", tags=["wallet"], response_model=WalletRequestResponse)
async def create_new_wallet_info(wallet_address: str, db_session: AsyncSession = Depends(get_db)):
    """
    Создает новую запись информации о кошельке Tron.

    Args:
        wallet_address: Адрес кошелька Tron
        db_session: Сессия базы данных

    Returns:
        Информация о кошельке
    """
    try:
        wallet_info = await get_wallet_info(wallet_address)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    wallet_request = await create_wallet_request(db_session, wallet_info)
    return wallet_request


@router.get("/wallet", response_model=List[WalletRequestResponse])
async def get_wallets(
        skip: int = 0,
        limit: int = 10,
        db_session: AsyncSession = Depends(get_db)
) -> List[WalletRequest]:
    """
    Получает список информации о кошельках.

    Args:
        skip: Количество записей для пропуска (для пагинации)
        limit: Максимальное количество записей для возврата
        db_session: Сессия базы данных

    Returns:
        Список информации о кошельках
    """
    wallet_requests = await get_wallet_requests(db_session, skip, limit)
    return wallet_requests
