import json
import os

from loguru import logger

from xcoder import run
from xcoder.config import config
from xcoder.features.update.download import download_update
from xcoder.localization import locale


def get_run_output(command: str):
    import tempfile

    temp_filename = tempfile.mktemp(".temp")

    del tempfile
    run(command, temp_filename)

    with open(temp_filename) as f:
        file_data = f.read()

    os.remove(temp_filename)

    return file_data


def get_pip_info(outdated: bool = False) -> list:
    output = get_run_output(
        f"pip --disable-pip-version-check list {'-o' if outdated else ''}"
    )
    output = output.splitlines()
    output = output[2:]
    packages = [package.split() for package in output]

    return packages


def get_tags(owner: str, repo: str):
    api_url = "https://api.github.com"

    import urllib.request

    tags = json.loads(
        urllib.request.urlopen(api_url + f"/repos/{owner}/{repo}/tags").read().decode()
    )
    tags = [
        {key: v for key, v in tag.items() if key in ["name", "zipball_url"]}
        for tag in tags
    ]

    return tags


def check_update():
    tags = get_tags(config.repo_owner, config.repo_name)

    if len(tags) > 0:
        latest_tag = tags[0]
        latest_tag_name = latest_tag["name"][1:]  # clear char 'v' at string start

        logger.info(locale.check_update)
        if config.version != latest_tag_name:
            logger.error(locale.not_latest)

            logger.info(locale.update_downloading)
            download_update(latest_tag["zipball_url"])
