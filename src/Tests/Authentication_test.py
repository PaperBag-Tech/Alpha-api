import json
import pytest
from .conftest import adminEmail, adminPassword

token: str

class TestAuthentication:
	@pytest.mark.order(1)
	def test_login(args, testSession):
		data = {
			"username" : adminEmail,
			"password" : adminPassword
		}
		response = testSession.post("/token", data)
		assert response.status_code == 200
		res = response.json()
		token = res["access_token"]
		assert res["token_type"] == "bearer"