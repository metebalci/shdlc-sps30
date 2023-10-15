clean:
	rm -rf dist

sdist: clean
	python setup.py sdist

pylint: 
	pylint shdlc_sps30/*.py

upload:
	twine upload dist/*
