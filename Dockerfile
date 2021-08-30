FROM python:3.9.6-buster

RUN apt-get update -y && \
    pip install pipenv --no-cache-dir && \
    git clone https://github.com/cyfronet-fid/oms-adapter-jira.git && \
    cd oms-adapter-jira && \
    pipenv install --system && \
    cd oms-adapter-jira/oms_jira/services && \
    sed -i "s|first_name: str| # first_name: str|g" mp.py && \
    sed -i "s|last_name: str| # last_name: str|g" mp.py && \
    sed -i "s|timestamp = datetime.datetime|timestamp: datetime.datetime|g"


ENV PYTHONPATH "${PYTHONPATH}:/oms-adapter-jira"

COPY . /src

WORKDIR /src

RUN pip install -r requirements/requirements.txt --no-cache-dir && \
    touch src/last_timestamp.txt

ENTRYPOINT [ "python3" ]

CMD [ "/src/src/app.py" ]
