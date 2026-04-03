from fastapi import FastAPI
from database import engine, Base
from routers import AuthenticationRouter, GenreRouter, MovieRouter, UserRouter 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lifeflix")

app.include_router(AuthenticationRouter.router)
app.include_router(UserRouter.router)
app.include_router(MovieRouter.router)
app.include_router(GenreRouter.router)
