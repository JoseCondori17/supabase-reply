import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import database, table, schema

app = FastAPI(
    title="Pinpom API",
    version="1.0.0"
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

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
    