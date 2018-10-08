FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /app/
WORKDIR /app/

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app/

RUN python manage.py makemigrations
RUN python manage.py collectstatic

# CMD python manage.py migrate \
#  && python manage.py loaddata fixtures/admin.json \
#  && python manage.py loaddata fixtures/skills.json \
#  && python manage.py runserver 0.0.0.0:80

CMD python manage.py migrate \
  && python manage.py loaddata fixtures/admin.json \
  && python manage.py loaddata fixtures/skills.json \
  && gunicorn codeproject.wsgi -b :80
