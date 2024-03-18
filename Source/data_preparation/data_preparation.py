import os
import pandas as pd
from pathlib import Path

import Source.logger as log

data_logger = log.app_logger(__name__)

"""
Data preparation functions.
The downloaded and extracted datasets
are turned into dataframes to be 
uploaded into the database.
"""

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
    Creates a pandas dataframe from a CSV file.
    Requires a name of the file.
    :return: a pandas dataframe of the CSV file.
    """
    path_to_file = os.path.join(PATH_TO_DATA, csv_file)
    dataframe = pd.read_csv(path_to_file)

    return dataframe


def change_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Changes the column names of the dataframe to their new column names.
    :param dataframe: a pandas dataframe to change column names
    :return: dataframe with new column names
    """
    new_names = {"Loan_ID": "loan_id",
                 "Gender": "gender",
                 "Married": "married",
                 "Dependents": "dependents",
                 "Education": "education",
                 "Self_Employed": "self_employed",
                 "ApplicantIncome": "applicant_income",
                 "CoapplicantIncome": "coapplicant_income",
                 "LoanAmount": "loan_amount",
                 "Loan_Amount_Term": "loan_amount_term",
                 "Credit_History": "credit_history",
                 "Property_Area": "property_area",
                 "Loan_Status": "loan_status"}
    dataframe.rename(columns=new_names, inplace=True)
    dataframe.reindex(columns=new_names)
    return dataframe


def kaggle_dataset_preparation(queue, event):
    """
    Setting up the sequence in which
    to execute data preparation functions.
    The csv files are turned into pandas DataFrame's
    and put into a queue.
    """
    while not event.is_set():
        try:
            csv_files = get_files_in_directory()
            data_logger.info('Files found in a directory: {}'.format(csv_files))

            for csv_file in csv_files:
                csv_to_df = create_dataframe(csv_file)
                new_col_names = change_column_names(csv_to_df)
                data_logger.info('A dataframe was created for a file: {}'.format(csv_file))
                queue.put([new_col_names, csv_file])
            print()
            event.set()
        except Exception as e:
            data_logger.error("An error occurred while creating a dataframe: {}\n".format(e))
