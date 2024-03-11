import os
import pandas as pd
from pathlib import Path

import Source.logger as log

data_logger = log.app_logger(__name__)

PATH_TO_DATA = Path(__file__).cwd() / 'Source/data/'


def get_files_in_directory() -> list:
    """
    Reads files in a set directory.
    Returns a list of names of files in the directory
    to be iterated through.
    :return: a list of file names in the directory
    """
    files_in_path = os.scandir(PATH_TO_DATA)

    list_of_files = []
    for file in files_in_path:
        if file.is_dir() or file.is_file() and file.name.endswith('.csv'):
            list_of_files.append(file.name)
    return list_of_files


def create_dataframe(csv_file: str) -> pd.DataFrame:
    """
    Creates a pandas dataframe from a JSON file.
    Requires a name of the file.
    """
    path_to_file = os.path.join(PATH_TO_DATA, csv_file)
    dataframe = pd.read_csv(path_to_file)

    return dataframe


def kaggle_dataset_preparation(queue, event):
    while not event.is_set():
        try:
            csv_files = get_files_in_directory()
            data_logger.info('Files found in a directory: {}'.format(csv_files))

            for csv_file in csv_files:
                csv_to_df = create_dataframe(csv_file)
                data_logger.info('A dataframe was created for a file: {}'.format(csv_file))
                queue.put([csv_to_df, csv_file])

            event.set()
        except Exception as e:
            data_logger.error("An error occurred while creating a dataframe: {}".format(e))
