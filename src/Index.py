from fastapi import FastAPI
from Database.Config import Base, engine
from API.V1.Main import router
import uvicorn

app = FastAPI(title="Alpha-API")

# configuring all the api routes
app.include_router(router)

# configuring database
Base.metadata.create_all(engine)


if __name__ == "__main__":
	uvicorn.run(app)