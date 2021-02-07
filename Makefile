build:
	docker-compose up -d
up:
	docker-compose up -d
ssh:
	docker exec -it blogapp /bin/bash
server:
	docker-compose run web python3 manage.py runserver
down:
	docker-compose down
flake8:
	docker-compose run web flake8 blog
test:
	docker-compose run web python3 manage.py test