FROM tensorflow/tensorflow:2.3.0-gpu

COPY requirements.txt /tmp/
RUN \
	pip install -r /tmp/requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8000/tcp

CMD [ "gunicorn", "--bind=0.0.0.0", "covid19backend:create_app()" ]
