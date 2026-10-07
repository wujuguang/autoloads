check:
	@ruff check --fix .
	@git add *
	@prek run

clean:
	@python -W ignore -m crons.framework
	@find . -name '*.pyc' -type f -exec rm -rf {} +
	@find . -name '__pycache__' -type d -exec rm -rf {} +
	@rm -rf logs html .pytest_cache *.log
