import json
import os


class DbConfig:
    def __init__(self, uri: str):
        self.uri = uri


class AppConfig:
    def __init__(self, db_config: DbConfig):
        self.db_config = db_config


def get_config(env: str) -> AppConfig:
    if env == "" or env is None:
        env = "local"

    file_name = f"{env}.json"
    current_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(current_location, file_name)) as json_config:
        config_data = json.load(json_config)

        return AppConfig(
            db_config=DbConfig(uri=config_data["db_config"]["uri"])
        )

