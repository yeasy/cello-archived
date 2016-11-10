.PHONY: \
	all \
	check \
	clean \
	log \
	logs \
	redeploy \
	restart \
	setup \

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

restart:
	bash scripts/restart.sh

setup:
	bash scripts/setup.sh
