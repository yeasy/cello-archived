.PHONY: \
	all \
	check \
	clean \
	log \
	logs \
	redeploy \
	restart \
	setup \

GREEN  := $(shell tput -Txterm setaf 2)
WHITE  := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)

HELP_FUN = \
	%help; \
	while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z\-]+)\s*:.*\#\#(?:@([a-zA-Z\-]+))?\s(.*)$$/ }; \
	print "usage: make [target]\n\n"; \
	for (sort keys %help) { \
	print "${WHITE}$$_:${RESET}\n"; \
	for (@{$$help{$$_}}) { \
	$$sep = " " x (32 - length $$_->[0]); \
	print "  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
	}; \
	print "\n"; }

help: ##@other Show this help.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

all: check

check:
	tox

clean:
	rm -rf .tox

# Use like "make log service=dashboard"
log:
	docker-compose logs -f ${service} --tail=100

logs:
	docker-compose logs -f --tail=100

# Use like "make redeploy service=dashboard"
redeploy:
	bash scripts/redeploy.sh ${service}

start: ##@Docker start service
	bash scripts/start.sh

stop: ##@Docker stop service
	bash scripts/stop.sh

npm-install: ##@NODEJS install packages needed by nodejs
	docker-compose -f docker-compose-npm-install.yml up

watch-mode: ##@NODEJS run build react js in watch mode
	docker-compose -f docker-compose-watch-mode.yml up

build-prod-js: ##@NODEJS run build react js in product
	docker-compose -f docker-compose-build-production-js.yml up

restart: stop start

setup:
	bash scripts/setup.sh
