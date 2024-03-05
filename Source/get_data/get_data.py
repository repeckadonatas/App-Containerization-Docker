import requests
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from queue import Queue


def get_data(url: str):
    response = requests.get(url)
    if

    with open(filename, mode='wb') as file:
        file.write(response.content)




url_template = ('https://www.kaggle.com/datasets/vikasukani/loan-eligible-dataset/data?select={filename}')
url_list = [url_template.format(filename='loan-test.csv'),
            url_template.format(filename='loan-train.csv')]

with ThreadPoolExecutor(max_workers=1) as executor:
    executor.map(get_data, url_list)
