import logging
import asyncio
from functools import wraps
from tronpy import AsyncTron
from tronpy.exceptions import AddressNotFound
from tronpy.providers import AsyncHTTPProvider

from app.core.config import settings
from app.schemas.wallet_request import WalletRequestCreate

API_KEY = settings.TRON_API_KEY
logger = logging.getLogger(__name__)


def retry_async(retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Попытка {attempt + 1}/{retries} не удалась: {str(e)}")
                    if attempt < retries - 1:
                        await asyncio.sleep(delay)
            raise last_exception

        return wrapper

    return decorator


@retry_async(retries=3, delay=2)
async def get_wallet_info(addr: str) -> WalletRequestCreate:
    async with AsyncTron(provider=AsyncHTTPProvider(api_key=API_KEY)) as client:
        try:
            account = await client.get_account(addr)
            account_resource = await client.get_account_resource(addr)

            balance = account.get('balance', 0) / 10 ** 6  # TRX имеет 6 знаков
            bandwidth = account_resource.get('freeNetLimit', 0)
            energy = account_resource.get('energyLimit', 0)

            logger.info(f"Успешно получена информация для кошелька {addr}")
            return WalletRequestCreate(
                wallet_address=addr,
                balance=balance,
                total_free_bandwidth=bandwidth,
                energy=energy,
            )

        except AddressNotFound:
            logger.error(f"Кошелек не найден: {addr}")
            raise ValueError("Account not found on-chain")
        except Exception as e:
            logger.error(f"Ошибка при запросе Tron API: {str(e)}", exc_info=True)
            raise RuntimeError(f"Ошибка при запросе Tron API: {str(e)}")
