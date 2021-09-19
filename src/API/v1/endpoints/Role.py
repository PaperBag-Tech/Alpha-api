from datetime import datetime
from sqlalchemy.orm import session
from fastapi import APIRouter, Depends, HTTPException
from typing import List

import Schemas.Role as RoleValidator
import Database.Config as dbConfig
import Models.Role as RoleModel
import API.Authentication as auth
import Database.Enums as Constants
import Models.User as UserModel


RoleRouter = APIRouter()

read = auth.RoleChecker(RoleModel.Role.__tablename__,"read")
write = auth.RoleChecker(RoleModel.Role.__tablename__,"write")
update = auth.RoleChecker(RoleModel.Role.__tablename__,"update")
delete = auth.RoleChecker(RoleModel.Role.__tablename__,"delete")

@RoleRouter.post("/",response_model=RoleValidator.RoleRead, status_code=201)
async def create(data: RoleValidator.RoleWrite, db: session = Depends(dbConfig.getDB), access: UserModel.User = Depends(write)):
	"""
		Create role record
	"""
	duplicateRole = db.query(RoleModel).filter(RoleModel.name == data.name).first()
	if duplicateRole != None:
		raise HTTPException(409, detail={"error" : "Duplicate entry"})
	permission = []
	for role in data.permissions:
		permission.append(f"{role.object}:{role.access}")
	permission = ",".join(permission)
	role = RoleModel.Role(name = data.name, type = Constants.UserRole(data.type), permissions= permission)
	db.add(role)
	db.commit()
	return (_convertRoleModelToRoleRead([role]))[0]

@RoleRouter.get("/permissions", status_code= 200)
async def GetAllPermissions(access: UserModel.User = Depends(read)):
	"""
		Gets all permissions list
	"""
	permissions = list()
	for tables in dbConfig.Base.metadata.tables.keys():
		permissions.append(f"{tables}:read")
		permissions.append(f"{tables}:write")
		permissions.append(f"{tables}:update")
		permissions.append(f"{tables}:delete")
	return permissions

@RoleRouter.put("/{id}", response_model=RoleValidator.RoleRead, status_code=200)
async def Update(id: int, data: RoleValidator.RoleWrite, db: session = Depends(dbConfig.getDB), access: UserModel.User = Depends(update)):
	"""
		Update role record by id
	"""
	role: RoleModel.Role = _getRole(id, db)
	role.name = data.name
	role.type = Constants.UserRole(data.type)
	permissionList = list()
	for permission in data.permissions:
		permissionList.append(f"{permission.object}:{permission.access}")
	role.permissions = ",".join(permissionList)
	role.updated_at = datetime.utcnow()
	db.commit()
	return (_convertRoleModelToRoleRead([role]))[0]

@RoleRouter.delete("/{id}", response_model=RoleValidator.RoleRead, status_code=202)
async def Delete(id: int, db: session = Depends(dbConfig.getDB), access: UserModel.User = Depends(delete)):
	"""
		Delets Role by id
	"""
	role = _getRole(id, db)
	db.delete(role)
	db.commit()
	return (_convertRoleModelToRoleRead([role]))[0]

@RoleRouter.get("/{id}", response_model=RoleValidator.RoleRead, status_code=200)
async def GetById(id: int, db: session = Depends(dbConfig.getDB), access: UserModel.User = Depends(read)):
	"""
		Gets Role by id
	"""
	role:RoleModel = _getRole(id, db)
	return (_convertRoleModelToRoleRead([role]))[0]

@RoleRouter.get("/", response_model=List[RoleValidator.RoleRead], status_code=200)
async def GetAll(db: session = Depends(dbConfig.getDB), access: UserModel.User = Depends(read)):
	"""
		Gets all Roles
	"""
	roles:list[RoleModel.Role] = db.query(RoleModel.Role).all()
	return _convertRoleModelToRoleRead(roles)

def _getRole(id: int, db: session):
	role = db.query(RoleModel.Role).filter(RoleModel.Role.id == id).first()
	if role == None:
		details = {"error" : f"Role record with id {id} is not found"}
		raise HTTPException(404, detail= details)
	return role

def _convertRoleModelToRoleRead(roles:List[RoleModel.Role]) -> List[RoleValidator.RoleRead]:
	roleReadList:list[RoleValidator.RoleRead] = roles
	for role in roleReadList:
		role.type = Constants.UserRole(role.type)
		permissionObjectList:list[RoleValidator.Permission] = list()
		permissionsList = role.permissions.split(',')
		for permission in permissionsList:
			permissionList = permission.split(":")
			permissionObject = RoleValidator.Permission(object=permissionList[0],access=permissionList[1])
			permissionObjectList.append(permissionObject)
		role.permissions = permissionObjectList
	return roleReadList	