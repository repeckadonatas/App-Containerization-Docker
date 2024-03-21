import os
from zipfile import ZipFile
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

import kaggle
import Source.logger as log

kaggle_logger = log.app_logger(__name__)

"""
Data download functions.
Data is downloaded from kaggle.com
and stored in a set location.
"""

KAGGLE_JSON_PATH = Path(__file__).cwd() / 'Source/.kaggle/'
PATH_TO_DATA = Path(__file__).cwd() / 'Source/data/'


def get_kaggle_credentials() -> os.environ:
    """
    Gets kaggle credentials from .env file.
    :return: environ
    """
    load_dotenv(find_dotenv('.env'))

    return os.environ


def get_data():
    """
    Gets data from kaggle.com using Kaggle API.
    The data is saved in a set folder.
    For authentication, Username and API key are retrieved
    either from kaggle.json file or from .env1 file.
    """
    try:
        os.environ['KAGGLE_CONFIG_DIR'] = str((KAGGLE_JSON_PATH / 'kaggle.json').absolute())
        os.chmod(os.environ['KAGGLE_CONFIG_DIR'], 600)

        api = kaggle.KaggleApi()
        api.authenticate()
        api.dataset_download_files('vikasukani/loan-eligible-dataset', path=PATH_TO_DATA)
        kaggle_logger.info('Downloaded Kaggle dataset.')

    except (Exception, IOError) as e:
        kaggle_logger.error('An exception occurred while downloading Kaggle dataset: {}'.format(e))


def get_files_in_directory() -> list:
    """
    Scans the directory and returns the names
    of all the files in it.
    :return: List of all files in the directory.
    """
    files_in_path = os.scandir(PATH_TO_DATA)

    list_of_files = []
    for file in files_in_path:
        if file.is_dir() or file.is_file():
            list_of_files.append(file.name)
    return list_of_files


def unzip_data(zip_file: str):
    """
    Extracts the files from a zip file.
    Saves extracted files in the same directory.
    """
    try:
        with ZipFile(PATH_TO_DATA / zip_file, 'r') as archive:
            archive.extractall(path=PATH_TO_DATA)
            archive.close()
        kaggle_logger.info('File unzipped successfully: {}\n'.format(archive))
    except FileNotFoundError:
        kaggle_logger.error('File(s) not found. Could not unzip anything.')


def kaggle_dataset_download():
    """
    This function sets up the correct execution sequence
    of data download functions.
    """
    get_data()
    files = get_files_in_directory()
    for file in files:
        if file.endswith('.zip'):
            unzip_data(file)
        elif file.endswith('.csv'):
            pass
        else:
            kaggle_logger.info('No files to unzip')
