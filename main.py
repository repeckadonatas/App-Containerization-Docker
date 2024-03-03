from pathlib import Path

import Source.logger as log
from Source.db_functions.db_functions import MyDatabase
from Source.db_functions.db_functions import env_config

main_logger = log.app_logger(__name__)

# Path(__file__).parent.absolute()

with MyDatabase() as db:

    try:
        env_config()
        db.create_table()
    except Exception as e:
        main_logger.error('Exception occurred: {}'.format(e))
