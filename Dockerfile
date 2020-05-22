FROM python:3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -i https://pypi.douban.com/simple -r requirements.txt

COPY . .

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD ["python","manage.py","runserver","0.0.0.0:8000"]