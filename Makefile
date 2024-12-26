.PHONY: test run migrate docker docker-superuser docker-test

test:
	python manage.py test

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

docker:
	docker-compose up --build

docker-superuser:
	docker-compose run app sh -c "python manage.py createsuperuser"

docker-test:
	docker-compose run app sh -c "python manage.py test"
