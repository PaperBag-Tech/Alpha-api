dev:
	cd src && uvicorn Index:app --reload && cd ..
test:
	pytest
	rm src/Tests/*.db
