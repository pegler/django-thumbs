test:
	flake8 thumbs --ignore=E501,E128
	coverage run --branch --source=thumbs `which django-admin.py` test --settings=tests.test_settings thumbs
	coverage report --omit=test*
