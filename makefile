dev:
	cd src && uvicorn Index:app --reload && cd ..
test:
	pytest -v
	rm src/Tests/*.db
migrate:
	cd src && alembic revision -m "$(msg)" && cd ..
upgradeDB:
	cd src && alembic upgrade head && cd ..
createAdmin:
	python src/Admin.py
