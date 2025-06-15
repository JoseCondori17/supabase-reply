import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from server.api.dependencies import admin_instance
from server.api.v1.endpoints import database, table, schema

# init instance
@asynccontextmanager
async def lifespan(app: FastAPI):
    from server.engine.executor import PinPom
    global admin_instance
    admin_instance = PinPom()
    yield

app = FastAPI(
    title="Pinpom API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(database.router, prefix="/database", tags=["database"])
app.include_router(table.router, prefix="/table", tags=["table"])
app.include_router(schema.router, prefix="/schema", tags=["schema"])
app.include_router(schema.router, prefix="/query", tags=["query"])

if __name__ == '__main__':
    uvicorn.run(
        "server.api.main:app",
        port=8000,
        reload=True
    )
    