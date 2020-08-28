.PHONY: run dist docker clean

run: docker
	docker run -it --rm -p 8080:80 covid19frontend

dist: clean
	docker run -it --rm -v $$PWD:/app -w /app -u $$UID:$$GID node sh -c 'npm install && npm run build'

docker: dist
	docker build . -t covid19frontend

clean:
	rm -rf dist
