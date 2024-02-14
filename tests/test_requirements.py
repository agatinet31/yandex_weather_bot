import os

from .conftest import infra_dir_path


class TestRequirements:
    def test_requirements(self):
        try:
            file_name = os.path.join(infra_dir_path, "requirements.prod")
            with open(file_name, "r") as f:
                requirements = f.read()
        except FileNotFoundError:
            assert False, "Проверьте, что добавили файл requirements.prod"

        pip_package = (
            "django",
            "djangorestframework",
            "gunicorn",
            "psycopg2-binary",
            "python-dotenv",
        )
        for package_name in pip_package:
            assert package_name in requirements, (
                f"Проверьте, что добавили {package_name} "
                "в файл requirements.prod"
            )
