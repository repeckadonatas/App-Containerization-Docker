# FinTech Loan Modelling


## About

This project is an exercise in building a working data pipeline model that would be later containerized for easier future replication on other machines and systems. The program retrieves two CSV files that are a part of **[Loan Eligible Dataset](https://www.kaggle.com/datasets/vikasukani/loan-eligible-dataset)** from Kaggle. After the data is downloaded, it is then transformed and prepared to be uploaded to the database. The program uses Threading as a concurrency method. Threading is suitable when looking to parallelize heavy I/O work, such as HTTP calls, reading from files and processing data.


## Tech Stack Used

* Programing language - **Python**;
* Servers and load balancing - for this project, data is stored locally on the machine;
* Data storage and querying - **PostgreSQL**;
* For testing data preparation functions - **Jupyter Notebook**;
* Data cleaning and normalization - **Pandas**;
* Package and dependency management - **Poetry**;
* Containerization - **Docker**


## How To Use The Program

### 1. Using manually locally

Prior to running the program, dependencies from `pyproject.toml` file should be installed. Use `Poetry` package to install project dependencies:
* `pip install poetry`
* `poetry install --no-root`

The basic usage on `Poetry` is **[here](https://python-poetry.org/docs/basic-usage/#installing-dependencies)**.
Once dependency installation is completed, the program can now be used. 

To use the program, run the _`main.py`_ file. Once started, the API data download will begin, followed by data preparation and then data upload to respective tables on a database.


### 2. Using Docker

To run the program in a Docker container, in the terminal window run `docker compose -f docker-compose.yaml up` command. The Docker compose YAML file should be on a target machine first. This will use **PostgreSQL** database image from docker.io and the image of the program from Docker Hub.

\
**Note:**

Every time the program runs, a log file is created in `logs` folder for that day. Information about any subsequent run is appended to the log file of that day. The program logs every data download, data transformation and data upload to the database. Errors are also logged into the same log file for the current day of the run. 

- To restart the program, run _`main.py`_ again.

### **Important:**

1. **For database connection:**

To connect to the database, the `Source/db_functions/db_functions.py` file needs to read these values from `.env` file:

|                             |
|-----------------------------|
| PGUSER = db_username        | 
| PGPASSWORD = user_password  | 
| PGHOST = host_name          |
| PGPORT = port               |
| PGDATABASE =  database_name |
\
1.1. **For PostgreSQL Docker image:**

When using Docker, **PostgreSQL** needs POSTGRES_PASSWORD environment variable to be passed. For this reason the YAML file reads POSTGRES_PASSWORD environment variable from `.env` file.

\
2. **For Kaggle API to work:**

Kaggle API usage is set up using the official Kaggle **[documentation](https://www.kaggle.com/docs/api)** (**[Kaggle GitHub](https://github.com/Kaggle/kaggle-api)**). Kaggle API requires a **kaggle.json** file to be stored in a home directory. For Windows it is `C:\Users\<user_name>\.kaggle`. For Unix systems it is `~/.kaggle`. The file can be generated by signing up to Kaggle and going into your account settings. The code implements a workaround for this JSON file location, but it might not work properly (might be a Kaggle API problem). For this reason, the Dockerfile copies the **kaggle.json** file from the source of the program to `/home/.kaggle/` location in Docker image, so no problems should occur. For redundancy and workaround reasons, `.env` file also needs to contain **kaggle.json** credentials:

|                                   |
|-----------------------------------|
| KAGGLE_USERNAME = kaggle_username | 
| KAGGLE_KEY = kaggle_api_key       |

\
**Note:**

When using the code manually locally, store the `.env` file in `Source/credentials/` folder to connect to the database and use the Kaggle API with no issues. Also make sure that **kaggle.json** file is stored in a home directory as well as in `Source/.kaggle/`. For Windows the home directory is `C:\Users\<user_name>\.kaggle`. For Unix systems it is `~/.kaggle`.


## Input Dataset Preparation

A successful response to an API call produces a ZIP file that is then stored in `Source/data/` folder. Then the ZIP file contents are extracted in the same location.

There is only one (1) change done to both dataframes of CSV data - the names of the columns are changed to conform to snake case.


## Concurrency method used

The program uses Threading as concurrency method to fetch, transform and upload the data. Threading is suitable when looking to parallelize heavy I/O work, such as HTTP calls, reading from files and processing data. 

Here, Python's own `threading` and `concurrent.futures` modules are used. The `concurrent.futures` module provides a high-level interface for asynchronously executing callables. The asynchronous execution is performed with threads using `threading` module.
The `concurrent.futures` module allows for an easier way to run multiple tasks simultaneously using multi-threading to go around GIL limitations.


Using **ThreadPoolExecutor** subclass uses a pool of threads to execute calls asynchronously. All threads enqueued to **ThreadPoolExecutor** will be joined before the interpreter can exit.
