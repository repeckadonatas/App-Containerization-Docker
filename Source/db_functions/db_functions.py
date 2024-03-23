import pandas as pd
from os import environ
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.engine import URL
from sqlalchemy import create_engine, Table, Column, String, Integer, Float, MetaData

import Source.logger as log

db_logger = log.app_logger(__name__)

"""
Database connection functions.
Used to create a connection with a database
and pass data to it.
"""


def env_config():
    """
    Gets database connection credentials from .env file.
    :return: environ
    """
    load_dotenv(find_dotenv('.env', usecwd=True))

    return environ


class KaggleDataDatabase:

    def __init__(self):
        """
        Retrieves parsed config parameters from .env1 file.
        Creates database URL using parsed configuration variables.
        """
        try:
            self.params = env_config()
            self.db_url = URL.create('postgresql+psycopg',
                                     username=self.params.get('PGUSER'),
                                     password=self.params.get('PGPASSWORD'),
                                     host=self.params.get('PGHOST'),
                                     port=self.params.get('PGPORT'),
                                     database=self.params.get('PGDATABASE'))
        except Exception as err:
            db_logger.error("A configuration error has occurred: %s", err)

    def __enter__(self):
        """
        Creates a connection to the database when main.py is run.
        Creates a connection engine and sets autocommit flag to True.
        :return: connection to a database
        """
        try:
            self.engine = create_engine(self.db_url, pool_pre_ping=True)
            self.conn = self.engine.connect().execution_options(autocommit=True)

            db_logger.info("Connected to the database")
        except (Exception, AttributeError) as err:
            db_logger.error("The following connection error has occurred: %s", err)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the connection to the database once the program has finished.
        :param exc_type: exception type
        :param exc_val: exception value
        :param exc_tb: exception traceback
        """
        try:
            if self.conn is not None:
                self.conn.close()

                db_logger.info('Connection closed.')
            elif exc_val:
                raise

        except (Exception, AttributeError, exc_type, exc_val, exc_tb) as err:
            db_logger.error("Connection was not closed: %s", err)

    def create_tables(self):
        """
        Creates tables in a database if they do not exist.
        Returns a list of tables in a database.
        """
        try:
            self.metadata = MetaData()
            self.loan_test_table = Table(
                'loan_test',
                self.metadata,
                Column('loan_id', String(10)),
                Column('gender', String(10)),
                Column('married', String(5)),
                Column('dependents', Integer()),
                Column('education', String(15)),
                Column('self_employed', String(5)),
                Column('applicant_income', Integer()),
                Column('coapplicant_income', Integer()),
                Column('loan_amount', Float()),
                Column('loan_amount_term', Float()),
                Column('credit_history', Float()),
                Column('property_area', String(10))
            )

            self.loan_train_table = Table(
                'loan_train',
                self.metadata,
                Column('loan_id', String(10)),
                Column('gender', String(10)),
                Column('married', String(5)),
                Column('dependents', Integer()),
                Column('education', String(15)),
                Column('self_employed', String(5)),
                Column('applicant_income', Integer()),
                Column('coapplicant_income', Integer()),
                Column('loan_amount', Float()),
                Column('loan_amount_term', Float()),
                Column('credit_history', Float()),
                Column('property_area', String(10)),
                Column('loan_status', String(2))
            )

            for table, metadata in self.metadata.tables.items():
                if self.engine.dialect.has_table(self.conn, table):
                    db_logger.info('Table "{}" already exists.'.format(table))
                else:
                    metadata.create(self.engine, checkfirst=True)
                    db_logger.info('Table "{}" was created successfully.'.format(table))

            self.conn.rollback()
        except Exception as e:
            db_logger.error("An error occurred while creating a table: {}".format(e))
            self.conn.rollback()

    def get_tables_in_db(self):
        """
        Returns a list of all the tables in the database.
        """
        table_list = []
        for table, metadata in self.metadata.tables.items():
            if self.engine.dialect.has_table(self.conn, table):
                table_list.append(table)
        db_logger.info('Table(s) found in a database: {}'.format(table_list))

        return table_list

    def load_to_database(self, dataframe: pd.DataFrame, table_name: str):
        """
        Function to load the data of a dataframe to a specified table in the database.
        :param dataframe: dataframe to load data from.
        :param table_name: table to load the data to.
        """
        try:
            dataframe.to_sql(table_name, con=self.engine, if_exists='replace', index=False)
        except Exception as e:
            db_logger.error("An error occurred while loading the data: {}. Rolling back the last transaction".format(e))
            self.conn.rollback()


def kaggle_dataset_upload_to_db(queue, event):
    """
    Setting up the sequence in which
    to execute data upload to database.
    The pandas DataFrame's of the CSV files
    are taken from a queue.
    The dataframe is then loaded into a corresponding
    table in the database.
    """
    with KaggleDataDatabase() as db:
        try:
            db.create_tables()

            db_tables = db.get_tables_in_db()
            while not event.is_set() or not queue.empty():
                for table in db_tables:
                    dataframe, file_name = queue.get()
                    if file_name == 'loan_test.csv':
                        db.load_to_database(dataframe=dataframe, table_name=table)
                        db_logger.info('Dataframe "{}" loaded to a table "{}"'.format(file_name, table))
                    else:
                        db.load_to_database(dataframe=dataframe, table_name=table)
                        db_logger.info('Dataframe "{}" loaded to a table "{}"'.format(file_name, table))
                    queue.task_done()
        except Exception as e:
            db_logger.error("An error occurred while loading the data: {}.".format(e))
