import json
import pytest

class TestCategory:
	def test_CreateCategory(args,testSession):
		data = {
  			"name": "Test Name",
  			"desp": "Test Desp"
		}
		response = testSession.post("/category/", json.dumps(data))
		assert response.status_code == 201
		res = response.json()
		TestCategory.checkData(res, data)

	def test_GetAllCategory(args, testSession):
		response = testSession.get("/category/")
		assert response.status_code == 200

	def test_GetCategoryById(args, testSession):
		response = testSession.get("/category/1")
		assert response.status_code == 200 or response.status_code == 404
	
	def test_UpdateCategory(args, testSession):
		data = {
			"name" : "Test Name - edit",
			"desp" : "Test desp - edit "
		}
		response = testSession.put("/category/1", json.dumps(data))
		assert response.status_code == 200
		res = response.json()
		TestCategory.checkData(res, data)
	
	@pytest.mark.order(-1)
	def test_DeleteCategory(args, testSession):
		response = testSession.delete("/category/1")
		assert response.status_code == 202 or response.status_code == 404

	def checkData(res, data):
		assert res["name"] == data["name"]
		assert res["desp"] == data["desp"]
		
