import shutil
import os

file_to_copy = './docker-compose.override.yml'

os.makedirs('./docker_test', exist_ok=True)
shutil.copy(file_to_copy, './docker_test')