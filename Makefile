.PHONY: typehint
typehint:
	mypy --ignore-missing-imports netdis/
.PHONY: lint
lint:
	pylint netdis/
.PHONY: checklist
checklist: lint typehint
.PHONY: isort
isort:
	isort netdis/
.PHONY: format
format:
	yapf --style='{based_on_style: pep8, indent_width: 4, column_limit=120}' -ir netdis/
.PHONY: clean
clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr
	find . -type d -name .mypy_cache | xargs rm -fr
	