import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as reporte_router
from app.polling import polling_periodico

app = FastAPI(
    title="Reporte Service",
    docs_url="/reportes/docs",
    openapi_url="/reportes/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reporte_router, prefix="/reportes")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(polling_periodico(intervalo_segundos=30))

@app.get("/")
def read_root():
    return {"message": "Reporte Service Running"}
