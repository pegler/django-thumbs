test:
	flake8 thumbs --ignore=E501,E128
	coverage run --branch --source=thumbs `which django-admin.py` test --settings=thumbs.test_settings
	coverage report --omit=test* -m

.PHONY: test