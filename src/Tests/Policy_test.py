import json
from src.API.V1.endpoints.Policy import PolicyRouter

class TestPolicy:

	def test_CreatePolicy(args,testSession):
		data = {
			"codeName": "POL001",
			"title": "Policy No 1",
			"desp": "Policy desp",
			"categoryId": 1,
			"details": "<b> Policy details </b>"
			}
		response = testSession.post("/policy/", json.dumps(data))
		assert response.status_code == 201
		res = response.json()
		TestPolicy.checkData(res,data)

	def test_GetAllPolicy(args, testSession):
		response = testSession.get("/policy/")
		assert response.status_code == 200

	def test_GetPolicyById(args, testSession):
		response = testSession.get("/policy/1")
		assert response.status_code == 200 or response.status_code == 404
	
	def test_UpdatePolicy(args, testSession):
		data = {
			"codeName": "POL001-edit",
			"title": "Policy No 1-edit",
			"desp": "Policy desp-edit",
			"categoryId": 1,
			"details": "<b> Policy details - edit </b>"
		}
		response = testSession.put("/policy/1", json.dumps(data))
		assert response.status_code == 200
		res = response.json()
		TestPolicy.checkData(res, data)

	def test_DeleteCategory(args, testSession):
		response = testSession.delete("/policy/1")
		assert response.status_code == 202 or response.status_code == 404

	
	def checkData(res, data):
		assert res["codeName"] == data["codeName"]
		assert res["title"] == data["title"]
		assert res["desp"] == data["desp"]
		assert res["details"] == data["details"]
		assert res["categoryId"] == data["categoryId"]
