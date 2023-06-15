FROM python:3.9.13

RUN mkdir /CFT

WORKDIR /CFT

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#RUN chmod a+x docker/*.sh
