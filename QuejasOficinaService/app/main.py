from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Quejas Oficina Service",
    docs_url="/quejas/oficina/docs",
    openapi_url="/quejas/oficina/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router, prefix="/quejas/oficina")



@app.get("/")
def read_root():
    return {"message": "Quejas Oficina Service Running"}
