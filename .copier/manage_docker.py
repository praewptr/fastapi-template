import shutil
import os
from pathlib import Path
import json


def copy_file(source, destination):
    shutil.copy(source, destination)


def create_empty_file(destination):
    with open(destination, 'w') as f:
        pass  # Create an empty file


answers_path = Path(__file__).parent / ".copier-answers.yml"
answers = json.loads(answers_path.read_text())

os.makedirs('./docker_test', exist_ok=True)

if answers.get('traefik', False):
    copy_file('./docker-compose.override.yml', './docker_test')
    copy_file('./docker-compose.yml', './docker_test')
    copy_file('./docker-compose.postgres.yml', './docker_test')
    copy_file('./docker-compose.traefik.yml', './docker_test')
else:
    create_empty_file('./docker_test/docker-compose.override.yml')
    create_empty_file('./docker_test/docker-compose.yml')
    create_empty_file('./docker_test/docker-compose.postgres.yml')
    create_empty_file('./docker_test/docker-compose.traefik.yml')
