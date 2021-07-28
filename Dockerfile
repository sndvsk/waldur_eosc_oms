FROM python:3.9.6-buster

#MAINTANER Your Name "youremail@domain.tld"

RUN apt-get update -y && \
    pip install pipenv && \
    git clone https://github.com/cyfronet-fid/oms-adapter-jira.git && \
    cd oms-adapter-jira && \
    pipenv install --dev


ENV PYTHONPATH "${PYTHONPATH}:/oms-adapter-jira"

COPY . /src

WORKDIR /src

RUN pip install -r requirements/requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "/src/src/app.py" ]
