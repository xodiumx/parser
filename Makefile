init-parser:
	cd src && docker-compose up -d --build

init: init-parser init-superset

init-superset:
	cd superset/ && docker-compose -f docker-compose-non-dev.yml up -d --build