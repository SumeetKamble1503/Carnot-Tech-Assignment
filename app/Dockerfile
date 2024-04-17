
FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

# # Set environment variables
# ENV FLASK_DEBUG 1
# ENV FLASK_RUN_PORT 5000

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

CMD ["python", "app.py"]