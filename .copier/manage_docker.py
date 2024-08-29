import shutil
import os
from pathlib import Path
import json


def copy_file(source, destination):
    shutil.copy(source, destination)


answers_path = Path(__file__).parent / ".copier-answers.yml"
answers = json.loads(answers_path.read_text())
for key, value in answers.items():
    if key == 'traefik':
        if value:
            os.makedirs('./docker_test', exist_ok=True)

            copy_file('./docker-compose.override.yml', './docker_test')
            copy_file('./docker-compose.yml', './docker_test')
            copy_file('./docker-compose.postgres.yml', './docker_test')
            copy_file('./docker-compose.traefik.yml', './docker_test')
