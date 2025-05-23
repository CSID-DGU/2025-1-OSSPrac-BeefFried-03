FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY uwsgi.ini /etc/uwsgi/uwsgi.ini

COPY requirements.txt /app/requirements.txt

COPY ./ /app

RUN pip install --no-cache-dir -r /app/requirements.txt