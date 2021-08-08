from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import session
from Schemas.Editor import EditorRead, EditorWrite, EditorBase, EditorPassword, EditorLogin
from typing import List 
from datetime import datetime
from Database.Config import getDB


EditorRouter = APIRouter()

@EditorRouter.get("/", response_model=List[EditorRead], status_code=200)
async def GetAll(db: session = Depends(getDB)):
	pass

@EditorRouter.post("/", response_model=EditorRead, status_code=201)
async def Create(data: EditorWrite ,db: session = Depends(getDB)):
	pass

@EditorRouter.get("/{id}", response_model=EditorRead, status_code=200)
async def GetById(id: int, db: session = Depends(getDB)):
	pass

@EditorRouter.put("/{id}", response_model=EditorRead, status_code=200)
async def Update(id: int, data: EditorBase, db: session = Depends(getDB)):
	pass

@EditorRouter.delete("/{id}", response_model=EditorRead, status_code=202)
async def Delete(id: int, db: session = Depends(getDB)):
	pass

@EditorRouter.put("/changepassword", response_model=bool, status_code=200)
async def ChangePassword(id: int, data:EditorPassword, db:session = Depends(getDB)):
	return True

@EditorRouter.get("/Login")
async def EditorLogin(data: EditorLogin, db: session = Depends(getDB)):
	pass