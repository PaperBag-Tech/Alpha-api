from fastapi import FastAPI
from Database.Config import Base, engine
from API.v1.api import router

app = FastAPI(title="AlphaAPI")


@app.get("/")
def Index():
	return {"Title":"Go to /docs for more info."}

# configuring all the api routes
app.include_router(router)

# configuring database
Base.metadata.create_all(engine)
