import json
import os
from pathlib import Path
from typing import LiteralString

_LIBRARY_DIRECTORY = Path(__file__).parent


class Config:
    DEFAULT_LANGUAGE: LiteralString = "en-EU"

    REPO_OWNER: LiteralString = "xcoder-tool"
    REPO_NAME: LiteralString = "xcoder"

    config_path = _LIBRARY_DIRECTORY / "config.json"

    def __init__(self):
        self.config_items = (
            "initialized",
            "repo_owner",
            "repo_name",
            "version",
            "language",
            "has_update",
            "last_update",
            "auto_update",
            "should_render_movie_clips",
        )

        self.initialized: bool = False
        self.repo_owner: str = Config.REPO_OWNER
        self.repo_name: str = Config.REPO_NAME
        self.version = None
        self.language: str = Config.DEFAULT_LANGUAGE
        self.has_update: bool = False
        self.last_update: int = -1
        self.auto_update: bool = False
        self.should_render_movie_clips: bool = False

        self.load()

    def toggle_auto_update(self) -> None:
        self.auto_update = not self.auto_update
        self.dump()

    def change_language(self, language: str) -> None:
        self.language = language
        self.dump()

    def load(self) -> None:
        if os.path.isfile(self.config_path):
            with open(self.config_path) as config_file:
                config_data = json.load(config_file)
                for key, value in config_data.items():
                    setattr(self, key, value)

    def dump(self) -> None:
        with open(self.config_path, "w") as config_file:
            json.dump(
                {item: getattr(self, item) for item in self.config_items}, config_file
            )

    def get_repo_url(self) -> str:
        return f"https://github.com/{self.repo_owner}/{self.repo_name}"


config = Config()
