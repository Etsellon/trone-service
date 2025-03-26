import uvicorn
from fastapi import FastAPI

from app.api.v1.endpoints.tron_wallet_router import router as tron_wallet_router

app = FastAPI(
    title='Tron Wallets Collector',
    description='Сервис для сбора и хранения информации о кошельках Tron',
)

app.include_router(tron_wallet_router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
