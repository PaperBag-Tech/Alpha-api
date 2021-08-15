from datetime import datetime
from sqlalchemy.orm import session
from fastapi import APIRouter, Depends, HTTPException
from Schemas.Role import RoleRead, RoleWrite, Permission
from Database.Config import getDB
from Models.Role import Base, Role as RoleModel
from API.Authentication import RoleChecker
from typing import List

RoleRouter = APIRouter()

read = RoleChecker(RoleModel.__tablename__,"read")
write = RoleChecker(RoleModel.__tablename__,"write")
update = RoleChecker(RoleModel.__tablename__,"update")
delete = RoleChecker(RoleModel.__tablename__,"delete")

@RoleRouter.post("/",response_model=RoleRead, status_code=201)
async def create(data: RoleWrite, db: session = Depends(getDB), access: bool = Depends(write)):
	"""
		Create role record
	"""
	permission = []
	for role in data.permissions:
		permission.append(f"{role.object}:{role.access}")
	permission = ",".join(permission)
	role = RoleModel(name = data.name, desp = data.desp, permissions= permission)
	db.add(role)
	db.commit()
	return role

@RoleRouter.get("/permissions", status_code= 200)
async def GetAllPermissions(db: session = Depends(getDB), access: bool = Depends(read)):
	"""
		Gets all permissions list
	"""
	permissions = list()
	for tables in Base.metadata.tables.keys():
		permissions.append(f"{tables}:read")
		permissions.append(f"{tables}:write")
		permissions.append(f"{tables}:update")
		permissions.append(f"{tables}:delete")
	return permissions

@RoleRouter.put("/{id}", response_model=RoleRead, status_code=200)
async def Update(id: int, data: RoleWrite, db: session = Depends(getDB), access: bool = Depends(update)):
	"""
		Update role record by id
	"""
	role: RoleModel = _getRole(id, db)
	role.name = data.name
	permissionList = list()
	for permission in data.permissions:
		permissionList.append(f"{permission.object}:{permission.access}")
	role.permissions = ".".join(permissionList)
	role.updated_at = datetime.utcnow()
	db.commit()

@RoleRouter.delete("/{id}", response_model=RoleRead, status_code=202)
async def Delete(id: int, db: session = Depends(getDB), access: bool = Depends(delete)):
	"""
		Delets Role by id
	"""
	role = _getRole(id, db)
	db.delete(role)
	db.commit()
	return role

@RoleRouter.get("/{id}", response_model=RoleRead, status_code=200)
async def GetById(id: int, db: session = Depends(getDB), access: bool = Depends(read)):
	"""
		Gets Role by id
	"""
	role:RoleModel = _getRole(id, db)
	return (_convertRoleModelToRoleRead([role]))[0]

@RoleRouter.get("/", response_model=List[RoleRead], status_code=200)
async def GetAll(db: session = Depends(getDB), access: bool = Depends(read)):
	"""
		Gets all Roles
	"""
	roles:list[RoleModel] = db.query(RoleModel).all()
	return _convertRoleModelToRoleRead(roles)

def _getRole(id: int, db: session):
	role = db.query(RoleModel).filter(RoleModel.id == id).first()
	if role == None:
		details = {"error" : f"Role record with id {id} is not found"}
		raise HTTPException(404, detail= details)
	return role

def _convertRoleModelToRoleRead(roles:List[RoleModel]) -> List[RoleRead]:
	roleReadList:list[RoleRead] = roles
	for role in roleReadList:
		permissionObjectList:list[Permission] = list()
		permissionsList = role.permissions.split(',')
		for permission in permissionsList:
			permissionList = permission.split(":")
			permissionObject = Permission(object=permissionList[0],access=permissionList[1])
			permissionObjectList.append(permissionObject)
		role.permissions = permissionObjectList
	return roleReadList	