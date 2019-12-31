.PHONY: init
init: start_services
	@echo "Initiliazing application's data and state"
	./manage.py makemigrations
	./manage.py migrate
	./manage.py loaddata 000_site_dev
	./manage.py loaddata 001_admin
	@make services
	@echo "\nAddress: http://localhost:8000/admin"
	@echo "Credentials:\n  - user: admin@admin.org\n  - pass: 123"

.PHONY: start_services
start_services:
	docker-compose -f conf/docker-compose_dev.yml up -d

.PHONY: services
services:
	docker-compose -f conf/docker-compose_dev.yml ps

.PHONY: down
down:
	rm -f db.sqlite3

.PHONY: build
build:
	docker build -f conf/Dockerfile -t app-mercado-pago .

.PHONY: publish
publish:
	docker tag app-mercado-pago 871800672816.dkr.ecr.us-east-1.amazonaws.com/app-mercado-pago
	docker start awsecr
	docker exec -ti awsecr push app-mercado-pago
