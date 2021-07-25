from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schema import Policy, Category

app = FastAPI()
AuthScheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def Index():
	return {"Title":"Index"}

# login 
@app.post("/token")
def token(formData: OAuth2PasswordRequestForm = Depends()):
	pass

# policies

@app.post("/policy")
def CreatePolicy(data:Policy, token:str = Depends(AuthScheme)):
	pass

@app.get("/policies")
def GetAllPolicies():
	pass

@app.get("policy/{id}")
def GetPolicyById(id:int):
	pass

@app.put("/policy/{id}")
def UpdatePolicyById(id:int,data:Policy,token:str = Depends(AuthScheme)):
	pass

@app.delete("/policy/{id}")
def DeletePolicyById(id:int, token:str = Depends(AuthScheme)):
	pass

# categories 

@app.post("/category")
def CreateCategory(data: Category, token:str = Depends(AuthScheme)):
	pass

@app.get("/categories")
def GetAllCategories():
	pass

@app.get("category/{id}")
def GetCategoryById(id:int):
	pass

@app.delete("category/{id}")
def DeleteCategoryById(id:int, token:str = Depends(AuthScheme)):
	pass

@app.put("category/{id}")
def UpdateCategoryById(id:int, data:Category, token:str = Depends(AuthScheme)):
	pass
