### Nothing to see here
Purely educational project made to learn how to work with Celery.

### Setup
Store env vars in env/.dev-sample
```
DEBUG=1
SECRET_KEY=secret_key
DJANGO_ALLOWED_HOSTS=*

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432

CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0

CHANNELS_REDIS=redis://redis:6379/0
```

### Run
```shell
docker-compose up -d --build
```