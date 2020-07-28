FROM python:3.7-slim-stretch
RUN apt-get -y update && apt-get -y install build-essential
RUN apt-get -y install gettext-base 
RUN mkdir /redis-test
COPY ./img.jpg /redis-test/
COPY ./settings.py /redis-test/
COPY ./redis_stream.py /redis-test/
COPY ./requirments.txt /redis-test/
WORKDIR /redis-test/
RUN pip3 install -r requirments.txt
CMD ["locust -f redis_stream.py"]
