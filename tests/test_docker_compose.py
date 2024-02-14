import os
import re

from .conftest import infra_dir_path


class TestDockerfileCompose:
    def test_docker_compose_file(self):
        try:
            file_name = os.path.join(infra_dir_path, "docker-compose.yaml")
            with open(file_name, "r") as f:
                docker_compose = f.read()
        except FileNotFoundError:
            assert False, (
                f"Проверьте, что в директорию {infra_dir_path} "
                "добавлен файл `docker-compose.yaml`"
            )
        assert re.search(r"image:\s+postgres:", docker_compose), (
            "Проверьте, что  в файл docker-compose.yaml "
            "добавлен образ postgres"
        )
