FROM python:3
MAINTAINER DevTeam DarthTrader "buergler@gmx.ch"

RUN pip install numpy
RUN pip install requests

ENV TERM=xterm-256color

ENV PYTHONPATH "${PYTHONPATH}:/home/DarthTrader"

# root dir
RUN mkdir /home/DarthTrader
WORKDIR /home/DarthTrader
