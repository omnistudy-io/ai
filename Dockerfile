FROM python:3.10

WORKDIR /app
RUN pip install virtualenv
RUN python3 -m venv venv
RUN . ./venv/bin/activate

COPY . .

RUN pip install -r ./requirements.txt
EXPOSE 8001

CMD ["python3", "server.py"]
