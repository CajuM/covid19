.PHONE: all clean docker

all: out docker
	docker run -it --rm --gpus all -u $$UID:$$GID -v $$PWD/out:/app/out covid19model

clean:
	rm -rf out

docker:
	docker build -t covid19model .

out: clean
	mkdir -p out
