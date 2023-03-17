
IMAGE_NAME=order_parser

reupload: docker-down docker-build

upload: docker-build
	docker logs test

docker-build:
	docker-compose up --build -d

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

git:
	git add .
	git commit -m $(COMMIT)
	git push