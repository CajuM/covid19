FROM tensorflow/tensorflow:2.3.0-gpu

RUN \
	apt-get update && \
	apt-get -y install git && \
	cd /usr/local/lib/python3.6/dist-packages && \
	ln -s tensorflow_gpu-2.3.0.dist-info tensorflow-2.3.0.dist-info

COPY requirements.txt /tmp/
RUN \
	pip install -r /tmp/requirements.txt

COPY . /app

WORKDIR /app/out

CMD [ "../covid19ak.py" ]
