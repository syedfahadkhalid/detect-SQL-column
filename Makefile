git_commit:
	$(eval GIT_COMMIT = $(shell git rev-parse --short HEAD))

python-requirements:
	chmod +x ops/*

pii-column-check: git_commit python-requirements
	chmod +x ops/pii_column_check/pii-column-check.sh
	ops/pii_column_check/pii-column-check.sh