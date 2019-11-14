FROM python:3.7

ADD . ${APP_ROOT}/app
WORKDIR ${APP_ROOT}/app

# Packages
RUN apt-get update && apt-get install -y wget libfreetype6-dev pkg-config libpng-dev x11-xserver-utils
#RUN bash -c 'xhost +local:root'

# Requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN mkdir -p /root/.streamlit

RUN bash -c 'echo -e "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > /root/.streamlit/credentials.toml'

EXPOSE 8501
EXPOSE 5000