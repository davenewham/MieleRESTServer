FROM python:3.13-slim-bookworm

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "Server.py" , "-b", "127.0.0.1", "-p", "5001" ]
