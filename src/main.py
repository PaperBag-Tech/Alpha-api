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

@app.post("/policy", tags=["Policy"])
def CreatePolicy(data:Policy, token:str = Depends(AuthScheme)):
	"""
	Creates new policy.
	"""
	pass

@app.get("/policies",tags=["Policy"])
def GetAllPolicies():
	"""
	Get all policies.
	"""
	pass

@app.get("policy/{id}",tags=["Policy"])
def GetPolicyById(id:int):
	"""
	Get policy by ID.
	"""
	pass

@app.put("/policy/{id}",tags=["Policy"])
def UpdatePolicyById(id:int,data:Policy,token:str = Depends(AuthScheme)):
	"""
	Update policy by ID.
	"""
	pass

@app.delete("/policy/{id}",tags=["Policy"], description="")
def DeletePolicyById(id:int, token:str = Depends(AuthScheme)):
	"""
	Delete a policy by ID.
	"""
	pass

# categories 

@app.post("/category", tags=["Category"])
def CreateCategory(data: Category, token:str = Depends(AuthScheme)):
	"""
	Creates a Category.
	"""
	pass

@app.get("/categories", tags=["Category"])
def GetAllCategories():
	"""
	Get all categories.
	"""
	pass

@app.get("category/{id}", tags=["Category"])
def GetCategoryById(id:int):
	"""
	Get category by ID.
	"""
	pass

@app.delete("category/{id}", tags=["Category"])
def DeleteCategoryById(id:int, token:str = Depends(AuthScheme)):
	"""
	Delete a category by ID.
	"""
	pass

@app.put("category/{id}", tags=["Category"])
def UpdateCategoryById(id:int, data:Category, token:str = Depends(AuthScheme)):
	"""
	Update category by ID.
	"""
	pass
