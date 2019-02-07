import os


def get_var(key: str) -> str:
    result = os.environ.get(key)
    if result is None:
        raise Exception(f'Where is no {key} in os environ.')
    else:
        return result


with open("./backend/local_settings.py", 'w') as f:
    f.write(f"""
DEBUG = True

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{get_var("BASE_NAME")}',
        'USER': '{get_var("USER_NAME")}',
        'PASSWORD': '{get_var("BASE_PASSWORD")}',
        'HOST': '{get_var("BASE_HOST")}',
        'PORT': '{get_var("BASE_PORT")}',
    }}
}}

BROKER_URL = "{get_var("BROKER_URL")}"

BASE_URL = "{get_var("BASE_URL")}"

ALLOWED_HOSTS = ['*']
""")
