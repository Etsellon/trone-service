from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet_request import WalletRequest
from app.schemas.wallet_request import WalletRequestCreate, WalletRequestResponse


async def create_wallet_request(
        db_session: AsyncSession,
        wallet_request: WalletRequestCreate
) -> WalletRequestResponse:
    """
    Создает новый запрос кошелька в базе данных.

    Args:
        db_session: Асинхронная сессия базы данных
        wallet_request: Данные для создания запроса кошелька

    Returns:
        Созданный запрос кошелька
    """
    new_wallet_request = WalletRequest(
        wallet_address=wallet_request.wallet_address,
        balance=wallet_request.balance,
        total_free_bandwidth=wallet_request.total_free_bandwidth,
        energy=wallet_request.energy,
    )
    db_session.add(new_wallet_request)
    await db_session.commit()
    await db_session.refresh(new_wallet_request)
    return new_wallet_request


async def get_wallet_requests(
        db_session: AsyncSession,
        skip: int = 0,
        limit: int = 10
) -> List[WalletRequest]:
    """
    Получает список запросов кошельков из базы данных.

    Args:
        db_session: Асинхронная сессия базы данных
        skip: Количество записей для пропуска (для пагинации)
        limit: Максимальное количество записей для возврата

    Returns:
        Список запросов кошельков, отсортированных по дате создания (новые в начале)
    """
    query = (
        select(WalletRequest)
        .order_by(WalletRequest.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    result = await db_session.execute(query)
    return result.scalars().all()
