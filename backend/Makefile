.PHONE: all clean docker

all: out docker
	docker run -it --rm -p 8000:8000 --gpus all -u $$UID:$$GID -v $$PWD/model:/app/model covid19backend

clean:
	rm -rf out

docker:
	docker build -t covid19backend .

out: clean
	mkdir -p out
