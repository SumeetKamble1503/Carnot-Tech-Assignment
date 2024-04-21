FROM python:3.9

ADD . /opt
WORKDIR /opt

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /opt

# Load environment variables from .env file
COPY .env /opt/.env

COPY ./deploy.sh /opt/deploy.sh

RUN chmod +x /opt/deploy.sh 

CMD ["python", "app.py"]
