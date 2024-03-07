import os
import Source.logger as log
import Source.get_data as data
from Source.db_functions.db_functions import MyDatabase


main_logger = log.app_logger(__name__)

# Path(__file__).parent.absolute()

try:
    data.get_data()
    data.unzip_data()
except Exception as e:
    main_logger.info('Error while trying to download from kaggle: {}'.format(e))

with MyDatabase() as db:

    try:
        db.create_table()
    except Exception as e:
        main_logger.error('Exception occurred: {}'.format(e))