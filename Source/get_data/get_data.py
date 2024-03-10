import json
import os
from zipfile import ZipFile
from pathlib import Path
from os import environ, path
from dotenv import load_dotenv

import kaggle
import Source.logger as log

kaggle_logger = log.app_logger(__name__)

KAGGLE_JSON_PATH = Path(__file__).cwd() / 'Source/.kaggle'
PATH_TO_DATA = Path(__file__).cwd() / 'Source/data/'


def get_kaggle_credentials():
    basedir = Path(__file__).cwd() / 'Source/credentials'
    dotenv_path = path.join(basedir, '.env')
    load_dotenv(dotenv_path, verbose=True)
    return environ


def get_data():
    try:
        environ['KAGGLE_CONFIG_DIR'] = str(KAGGLE_JSON_PATH / 'kaggle.json')
        os.chmod(environ['KAGGLE_CONFIG_DIR'], 600)

        if Path(KAGGLE_JSON_PATH / 'kaggle.json').is_file():
            with open(KAGGLE_JSON_PATH / 'kaggle.json', 'r', encoding='utf-8') as kaggle_file:
                kaggle_credentials = json.load(kaggle_file)
            kaggle_credentials.get('username')
            kaggle_credentials.get('key')
        else:
            get_kaggle_credentials().get('KAGGLE_USERNAME')
            get_kaggle_credentials().get('KAGGLE_KEY')

        kaggle.api.authenticate()
        kaggle.api.dataset_download_files('vikasukani/loan-eligible-dataset', path=PATH_TO_DATA)
        kaggle_logger.info('Downloaded Kaggle dataset.')

    except (Exception, IOError) as e:
        kaggle_logger.error('An exception occurred while downloading Kaggle dataset: {}'.format(e))


def get_files_in_directory():
    files_in_path = os.scandir(PATH_TO_DATA)

    list_of_files = []
    for file in files_in_path:
        if file.is_dir() or file.is_file():
            list_of_files.append(file.name)
    return list_of_files


def unzip_data():
    try:
        files_to_unzip = get_files_in_directory()
        for file in files_to_unzip:
            if len(files_to_unzip) < 1 or file.endswith('.zip'):
                with ZipFile(PATH_TO_DATA / file, 'r') as archive:
                    archive.extractall(path=PATH_TO_DATA)
                    archive.close()
                    return kaggle_logger.info('File unzipped successfully: {}'.format(archive))
            else:
                kaggle_logger.info('No files to unzip')
                break
    except FileNotFoundError:
        kaggle_logger.error('File(s) not found. Could not unzip anything.')


def kaggle_dataset_download():
    get_data()
    unzip_data()
