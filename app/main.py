from fastapi import FastAPI
from api import router
import uvicorn

app = FastAPI(
    title='captcha-service',
    docs_url='/_swagger'
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8080,
        workers=1
    )
