FROM python:alpine

ADD ./requirements.txt /opt/webapp-mysql/

WORKDIR /opt/webapp-mysql

RUN pip install -r requirements.txt && pip install awscli --upgrade

ADD . /opt/webapp-mysql

EXPOSE 81

CMD python /opt/webapp-mysql/app.py
