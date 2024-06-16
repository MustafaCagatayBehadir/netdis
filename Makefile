.PHONY: typehint
typehint:
	mypy --ignore-missing-imports common/
	mypy --ignore-missing-imports configuration/
	mypy --ignore-missing-imports discovery/
.PHONY: lint
lint:
	pylint common/*
	pylint configuration/*   
	pylint discovery/*
.PHONY: checklist
checklist: lint typehint
.PHONY: isort
isort:
	isort common/
	isort configuration/
	isort discovery/
.PHONY: format
format:
	yapf --style='{based_on_style: pep8, indent_width: 4, column_limit=120}' -ir common/
	yapf --style='{based_on_style: pep8, indent_width: 4, column_limit=120}' -ir configuration/
	yapf --style='{based_on_style: pep8, indent_width: 4, column_limit=120}' -ir discovery/
.PHONY: clean
clean:
	find common/ -type f -name "*.pyc" | xargs rm -fr
	find common/ -type d -name __pycache__ | xargs rm -fr
	find configuration/ -type f -name "*.pyc" | xargs rm -fr
	find configuration/ -type d -name __pycache__ | xargs rm -fr
	find discovery/ -type f -name "*.pyc" | xargs rm -fr
	find discovery/ -type d -name __pycache__ | xargs rm -fr
	sudo find ./ -type d -name .mypy_cache | xargs rm -fr
	