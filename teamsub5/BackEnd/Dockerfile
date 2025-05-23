# Dockerfile at BackEnd

FROM python:3

# python 컨테이너에서 사용되는 경로
WORKDIR /usr/src/app

COPY requirements.txt .           
RUN pip install -r requirements.txt

COPY . .   

EXPOSE 5000
CMD [ "python3", "main.py" ]