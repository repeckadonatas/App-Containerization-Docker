import os
from pathlib import Path
import Source.logger as log
import Source.get_data as data
from Source.db_functions.db_functions import KaggleDataDatabase
# import Source.db_functions as db

import concurrent.futures
import threading
import time
from queue import Queue


main_logger = log.app_logger(__name__)

# Path(__file__).parent.absolute()

start = time.perf_counter()

# with KaggleDataDatabase() as db:
#     db.create_tables()

this_event = threading.Event()
try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        tasks = [executor.submit(data.get_data(), this_event),
                 executor.submit(data.unzip_data(), this_event),
                 executor.submit(KaggleDataDatabase().create_tables(), this_event)]  # <-- cannot reach variables from .env

    concurrent.futures.wait(tasks)
except (Exception, ValueError) as e:
    main_logger.error('Exception occurred: {}'.format(e))

end = time.perf_counter()

main_logger.info(f'Process completed in {end - start} seconds')
