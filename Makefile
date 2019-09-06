shell:
	@~/.virtualenvs/bumpversion/bin/ipython

build:
	@~/.virtualenvs/bumpversion/bin/python setup.py sdist
	twine upload dist/*

build/test:
	~/.virtualenvs/bumpversion/bin/python setup.py sdist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose

