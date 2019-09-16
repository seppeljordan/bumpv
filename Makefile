shell:
	@~/.virtualenvs/bumpversion/bin/ipython

build:
	~/.virtualenvs/bumpversion/bin/bumpv bump $(part)
	@~/.virtualenvs/bumpversion/bin/python setup.py sdist

upload:
	twine upload dist/*
	rm -rf ./dist

install:
	@python3 -m venv ~/.bumpv
	@~/.bumpv/bin/pip install .
	@echo 'alias bumpv="~/.bumpv/bin/bumpv"'

release: build upload
