shell:
	@~/.virtualenvs/bumpversion/bin/ipython

build:
	~/.virtualenvs/bumpversion/bin/bumpv bump $(part)
	@~/.virtualenvs/bumpversion/bin/python setup.py sdist
	twine upload dist/*
	rm -rf ./dist
