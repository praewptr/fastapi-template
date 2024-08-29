import shutil
import os


def file_to_copy(file, target):
    shutil.copy(file, target)
    return {"copied_file": file}


os.makedirs('./docker_test', exist_ok=True)

file_to_copy('./docker-compose.override.yml', './docker_test')
file_to_copy('./docker-compose.yml', './docker_test')
file_to_copy('./docker-compose.postgres.yml', './docker_test')
file_to_copy('./docker-traefik.yml', './docker_test')
