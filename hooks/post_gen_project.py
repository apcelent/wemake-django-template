"""
Does the following:

1. Generates and saves random secret key
2. Removes the taskapp if celery isn't going to be used
3. Removes the .idea directory if PyCharm isn't going to be used
4. Copy files from /docs/ to {{ cookiecutter.project_name }}/docs/

A portion of this code was adopted from Django's standard crypto functions and
utilities, specifically:
    https://github.com/django/django/blob/master/django/utils/crypto.py

And from pydanny's cookiecutter-django:
    https://github.com/pydanny/cookiecutter-django
"""

import os
import random
import shutil
import string

# CHANGEME mark
CHANGEME = '__CHANGEME__'

# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False


def get_random_string(length=50):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    punctuation = string.punctuation.replace('"', '').replace("'", '')
    punctuation = punctuation.replace('\\', '')
    if using_sysrandom:
        return ''.join(random.choice(
            string.digits + string.ascii_letters + punctuation
        ) for i in range(length))

    print(
        "Cookiecutter Django couldn't find a secure pseudo-random number generator on your system."
        " Please change change your SECRET_KEY variables in conf/settings/local.py and env.example"
        " manually."
    )
    return CHANGEME


def create_secret_key(config_path):
    with open(config_path) as f:
        file_ = f.read()

    # Generate a SECRET_KEY that matches the Django standard
    SECRET_KEY = get_random_string()

    # Replace CHANGEME with SECRET_KEY
    file_ = file_.replace(CHANGEME, SECRET_KEY, 1)

    # Write the results to the file
    with open(config_path, 'w') as f:
        f.write(file_)


def copy_local_configuration():
    """
    This function copies local configuration from `.template`s
    to the actual files.
    """

    # Secret config:
    secret_template = os.path.join(
        PROJECT_DIRECTORY, 'config', 'secret.env.template'
    )
    secret_config = os.path.join(
        PROJECT_DIRECTORY, 'config', 'secret.env'
    )
    shutil.copyfile(secret_template, secret_config)
    create_secret_key(secret_config)

    # Local config:
    local_template = os.path.join(
        PROJECT_DIRECTORY, 'server',
        'settings', 'environments', 'local.py.template'
    )
    local_config = os.path.join(
        PROJECT_DIRECTORY, 'server',
        'settings', 'environments', 'local.py'
    )
    shutil.copyfile(local_template, local_config)


# def copy_docs():
#     """
#     This function copies docs from the root repository
#     to the result project.
#     """


def clean_docker_files():
    """
    This function removes all docker-related files.

    It is called when user does not want to include docker support.
    """
    dockerignore = os.path.join(PROJECT_DIRECTORY, '.dockerignore')
    docker_compose = os.path.join(PROJECT_DIRECTORY, 'docker-compose.yml')
    dockerfile = os.path.join(PROJECT_DIRECTORY, 'Dockerfile')

    os.remove(dockerignore)
    os.remove(docker_compose)
    os.remove(dockerfile)

copy_local_configuration()

{% if cookiecutter.docker != 'y' %}
clean_docker_files()
{% endif %}