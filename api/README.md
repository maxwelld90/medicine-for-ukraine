# medicine-for-ukraine API

## Requirements
- python3

## Run migration
```bash
python manage.py makemigrations
python manage.py makemigrations api_app
python manage.py migrate
python manage.py migrate api_app
```

## Debug mode

```bash
export MEDICINE_DEBUG=true
python manage.py runserver
```

## Run redis
Docker:
```bash
docker run --rm --name medicine-for-ukraine-redis -d -p 6379:6379 redis
```