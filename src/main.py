from fastapi import FastAPI

from src.config import settings

app = FastAPI()

print(settings.environment)


@app.get('/')
async def root():
    return {
        'message' : 'Hello World'
    }
