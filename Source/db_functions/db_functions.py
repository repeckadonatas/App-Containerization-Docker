#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd
import Source.db_con_config as dbc
import Source.logger as log
from sqlalchemy import URL, create_engine, text

db_logger = log.app_logger(__name__)

"""
Database connection functions.
Used to create a connection with a database
and pass data to it.
"""


class MyDatabase:

    def __init__(self):
        """
        Retrieves parsed config parameters from credentials.ini file.
        Creates database URL using parsed configuration variables.
        """
        try:
            self.params = dbc.get_config()
            self.db_url = URL.create('postgresql+psycopg',
                                     username=self.params['user'],
                                     password=self.params['password'],
                                     host=self.params['host'],
                                     port=self.params['port'],
                                     database=self.params['dbname'])
        except Exception as err:
            db_logger.error("A configuration error has occurred: %s", err)

    def __enter__(self):
        """
        Creates a connection to the database when main.py is run.
        Creates a connection engine and sets autocommit flag to True.
        :return: connection to a database
        """
        try:
            self.engine = create_engine(self.db_url)
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

    def create_table(self):
        """
        Creates a table in a database if it does not exist.
        Returns a list of tables in a database.
        """
        try:
            if self.engine.dialect.has_table(self.conn, 'weather_data'):
                db_logger.info('Table already exists.')
            else:
                self.weather_data = """CREATE TABLE IF NOT EXISTS weather_data (
                    id INT GENERATED ALWAYS AS IDENTITY UNIQUE,
                    longitude FLOAT, latitude FLOAT, country_id INT, country VARCHAR(5), city VARCHAR(50),
                    main_temp FLOAT, main_feels_like FLOAT, main_temp_min FLOAT, main_temp_max FLOAT, 
                    date_vilnius TIMESTAMP WITHOUT TIME ZONE, date_local TIMESTAMP, timezone INT, 
                    sunrise_local TIMESTAMP, sunset_local TIMESTAMP, weather_id INT, weather_main VARCHAR(20), 
                    weather_description VARCHAR(100), weather_icon VARCHAR(50), pressure INT, humidity INT, 
                    wind_speed FLOAT, wind_deg INT, clouds INT, visibility INT, base VARCHAR(20), 
                    sys_type INT, sys_id INT, cod INT);"""

                self.conn.execute(text(self.weather_data))
                db_logger.info('Table was created successfully.')

            self.tables_in_db = self.conn.execute(text("""SELECT relname FROM pg_class 
                                                       WHERE relkind='r' 
                                                       AND relname !~ '^(pg_|sql_)';""")).fetchall()

            db_logger.info('Table(s) found in a database: {}'.format(self.tables_in_db))
            self.conn.rollback()
        except Exception as e:
            db_logger.info("An error occurred while creating a table: {}".format(e))
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
            db_logger.info("An error occurred while loading the data: {}. Rolling back the last transaction".format(e))
            self.conn.rollback()
