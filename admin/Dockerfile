FROM python:3.5
MAINTAINER Baohua Yang "baohyang@cn.ibm.com"
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

# use this in development
CMD ["python", "app.py"]

# use this in product
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
