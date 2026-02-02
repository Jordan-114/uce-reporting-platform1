from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(
    title="Quejas Web Service",
    docs_url="/quejas-web/docs",
    openapi_url="/quejas-web/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas del dominio Quejas Web
app.include_router(router, prefix="/quejas-web")

# Health check / raíz
@app.get("/")
def read_root():
    return {"message": "Quejas Web Service Running"}
