from pathlib import Path
import pandas as pd
from os import environ, path
from dotenv import load_dotenv
import Source.logger as log
from sqlalchemy import URL, create_engine, text, Table, Column, Integer, String, MetaData

db_logger = log.app_logger(__name__)

"""
Database connection functions.
Used to create a connection with a database
and pass data to it.
"""


def env_config():
    basedir = Path(__file__).cwd() / 'Source/credentials'
    dotenv_path = path.join(basedir, '.env')
    load_dotenv(dotenv_path)

    return environ


class KaggleDataDatabase:

    def __init__(self):
        """
        Retrieves parsed config parameters from credentials.ini file.
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

        except (Exception, AttributeError) as err:
            db_logger.error("Connection was not closed: %s", err)

    def create_tables(self):
        """
        Creates a table in a database if it does not exist.
        Returns a list of tables in a database.
        """
        try:
            self.metadata = MetaData()
            self.loan_test_table = Table(
                'loan_test',
                self.metadata,
                Column('id', Integer, unique=True),
                Column('name', String)
            )

            self.loan_train_table = Table(
                'loan_train',
                self.metadata,
                Column('id', Integer, unique=True),
                Column('name', String)
            )

            if self.engine.dialect.has_table(self.conn, 'loan_test', 'loan_train'):
                db_logger.info('Table already exists.')
            else:
                self.metadata.create_all(self.engine)
                db_logger.info('Table "{}" was created successfully.'.format(self.metadata))

            self.tables_in_db = self.conn.execute(text("""SELECT relname FROM pg_class 
                                                                       WHERE relkind='r' 
                                                                       AND relname !~ '^(pg_|sql_)';""")).fetchall()
            db_logger.info('Table(s) found in a database: {}'.format(self.tables_in_db))
            self.conn.rollback()
        except Exception as e:
            db_logger.error("An error occurred while creating a table: {}".format(e))
            self.conn.rollback()

    def load_to_database(self, dataframe: pd.DataFrame, table_name: str):
        """
        Function to load the data of a dataframe to a specified table in the database.
        :param dataframe: dataframe to load data from.
        :param table_name: table to load the data to.
        """
        try:
            dataframe.to_sql(table_name, con=self.engine, if_exists='append', index=False)
        except Exception as e:
            db_logger.error("An error occurred while loading the data: {}. Rolling back the last transaction".format(e))
            self.conn.rollback()
