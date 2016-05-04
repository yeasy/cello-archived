FROM python:3.5
MAINTAINER Baohua Yang "baohyang@cn.ibm.com"
#RUN apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential
#RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
#ENTRYPOINT ["python"]
COPY . /app

# use this in development
CMD ["python", "app.py"]

# use this in product
#CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:8080", "app:app"]
