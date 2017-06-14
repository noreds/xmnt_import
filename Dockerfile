FROM python:3
COPY . /opt/xmnt_import
WORKDIR /opt/xmnt_import
RUN pip install -r requirements.txt