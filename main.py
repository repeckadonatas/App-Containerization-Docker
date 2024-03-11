import Source.logger as log
import Source.get_data as dw
import Source.data_preparation as data
import Source.db_functions as db

import concurrent.futures
import threading
import time
from queue import Queue

main_logger = log.app_logger(__name__)

"""
Main program file to run the program
using concurrent.futures module.
The programs performance is also timed
and printed to out.
"""

start = time.perf_counter()

event = threading.Event()
queue = Queue(maxsize=2)
try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        tasks = [executor.submit(dw.kaggle_dataset_download()),
                 executor.submit(data.kaggle_dataset_preparation(queue, event)),
                 executor.submit(db.kaggle_dataset_upload_to_db(queue, event))]

    concurrent.futures.wait(tasks)
except (Exception, ValueError, FileNotFoundError, IOError) as e:
    main_logger.error('Exception occurred: {}'.format(e))

end = time.perf_counter()
print()
main_logger.info('Process completed in {} seconds'.format(end-start))

