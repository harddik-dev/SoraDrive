from fastapi import FastAPI
from .core.database import Base, engine
from .routers import auth_router
from .routers import file_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure Cloud Storage API")
app.include_router(auth_router.router)
app.include_router(file_router.router)