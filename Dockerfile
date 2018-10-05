FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /app/
WORKDIR /app/

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app/

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic

CMD python manage.py runserver 0.0.0.0:80
# CMD gunicorn codeproject.wsgi -b :80
