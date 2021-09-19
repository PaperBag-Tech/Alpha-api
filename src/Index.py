from fastapi import FastAPI
from Database.Config import Base, engine
from API.V1.Main import router
import uvicorn

import Database.Config as db
import API.V1.Main as v1
import API.Authentication as auth

app = FastAPI(title="Alpha-API")

# configuring all the api routes
app.include_router(v1.router, prefix="/v1")
app.include_router(auth.AuthenticationRouter, tags=["Authentication"])

# configuring database
Base.metadata.create_all(engine)


if __name__ == "__main__":
	uvicorn.run(app)