from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Routes import category, policy


app = FastAPI()
AuthScheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def Index():
	return {"Title":"Index"}

# login 
@app.post("/token")
def token(formData: OAuth2PasswordRequestForm = Depends()):
	pass


app.include_router(category.CategoryRouter)
app.include_router(policy.PolicyRouter)