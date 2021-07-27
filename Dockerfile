FROM ubuntu:20.04

#MAINTANER Your Name "youremail@domain.tld"

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

COPY . /src

WORKDIR /src

RUN pip install -r requirements/requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "/src/app.py" ]
