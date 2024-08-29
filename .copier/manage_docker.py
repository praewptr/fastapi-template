import shutil
import os


def copy_file(source, destination):
    shutil.copy(source, destination)


os.makedirs('./docker_test', exist_ok=True)

copy_file('./docker-compose.override.yml', './docker_test')
copy_file('./docker-compose.yml', './docker_test')
copy_file('./docker-compose.postgres.yml', './docker_test')
copy_file('./docker-compose.traefik.yml', './docker_test')
