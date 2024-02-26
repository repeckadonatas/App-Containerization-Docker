# FinTech Loan Modelling


## About(FIX)

This project is an exercise in building a working data pipeline model. The model sends API requests to openweathermap.org and retrieves weather data for 20 of the largest cities in Europe. The data is requested every hour. After the data is downloaded, it is then transformed and prepared to be uploaded to the database. The model uses Threading as a concurrency method. Threading is suitable when looking to parallelize heavy I/O work, such as HTTP calls, reading from files and processing data. 


## Tech Stack Used(FIX)

* Programing language - **Python**;
* Servers and load balancing - for this project, data is stored locally on the machine;
* Data storage and querying - **PostgreSQL**;
* For testing data preparation functions - **Jupyter Notebook**;
* Data cleaning and normalization - **Pandas**;
* Package and dependency management - **Poetry**


## How To Use The Program(FIX)

Prior to running the program, dependencies from `pyproject.toml` file should be installed. Use `Poetry` package to install project dependencies:
* `pip install poetry`
* `poetry install --no-root`

The basic usage on `Poetry` is **[here](https://python-poetry.org/docs/basic-usage/#installing-dependencies)**.
Once dependency installation is completed, the program can now be used. 

To use the program, run the _`main.py`_ file. Once started, the API data download will begin, followed by data preparation and then data upload to a table on a database.

The program runs automatically on a set schedule (once per hour every day). The schedule is set using cron. Alternatively, a schedule is also set using Windows Task Scheduler.

Currently, the program retrieves data of the 20 largest cities in **[Europe](https://en.wikipedia.org/wiki/List_of_European_cities_by_population_within_city_limits)** (source: Wikipedia). If the need arises to get the data for more cities, a name, country and the coordinates of a city must be placed in a text file in `Source/locations/locations.txt` in the same format as other cites (**especially** the coordinates).

Every time the program runs, a log file is created in `logs` folder for that day. Information about any subsequent run is appended to the log file of that day. The program logs every data download, data transformation and data upload to the database. Errors are also logged into the same log file for the current day of the run. 

**Note:** 
- To restart the program, run _`main.py`_ again.

### **Important:**

To connect to the database, the `Source/db_config/config.py` file needs to read these values from `credentials.ini` file:

| [name-of-credentials]    |
|--------------------------|
| user = user_name         | 
| password = user_password | 
| host = host_name         |
| port = port              |
| dbname =  database_name  |

Store the `credentials.ini` file in `Source/credentials/` folder to connect to the database with no issues.

For API connection, API key is needed. It should be stored in `api_key.txt` file in `Source/credentials/` folder.

The SQL queries to run analytical queries against weather data in a database are stored in `misc` folder. SQL uses PostgreSQL dialect. 


## Input Dataset Preparation(FIX)

A successful response to an API call produces a JSON file that is then stored in `Source/data/input` folder.

None of the data is removed. It is supplemented by an additional datetime column `date_vilnius`, which displays date and time adjusted to UTC+2 time zone.

There are three (3) changes done to data. First is how the data is displayed in the database after upload. The change consist of simple column reorder. The second change is to the names of the columns as after flattening the JSON file the column names do not match the snake case standard for naming. A third change is to local time. The column `date_local` displays a current datetime value of the city from where the weather data was taken.

Datetime values are converted to conform to **[ISO8601](https://www.iso.org/iso-8601-date-and-time-format.html)** standard.

In some cases, the JSON data can be missing some of the values of the table. In such cases those missing values are stored as NULL values.

Also, API response can contain a wrong value for `city` column in a table. After further inspection, it seems that the value is corresponding to a street name or a part of city. In such cases casting values to preferred names in SQL queries can remove the confusion. In such cases the coordinates are a source of truth.

Examples:
* **Madrid** sometimes can be presented as **Sol**;
* **Munich** sometimes can be presented as **Altstadt**;
* etc.

To check the coordinates, you can use a webpage such as **[this](https://www.gps-coordinates.net/)**.


## Concurrency method used(FIX)

The program uses Threading as concurrency method to fetch, transform and upload the data. Threading is suitable when looking to parallelize heavy I/O work, such as HTTP calls, reading from files and processing data. 

Here, Python's own `threading` and `concurrent.futures` modules are used. The `concurrent.futures` module provides a high-level interface for asynchronously executing callables. The asynchronous execution is performed with threads using `threading` module.
The `concurrent.futures` module allows for an easier way to run multiple tasks simultaneously using multi-threading to go around GIL limitations.


Using **ThreadPoolExecutor** subclass uses a pool of threads to execute calls asynchronously. All threads enqueued to **ThreadPoolExecutor** will be joined before the interpreter can exit.


## Creating Fake Weather Data(FIX)

To test some of the analytical functionality using SQL queries I created a SQL query to generate random data and upload it into a separate table. Later I created a view to join the table with fake data with table with real data. Then this view is used to run analytical SQL queries. The SQL to generate the data is stored in `misc/fake_weather_data_sql.sql` file.


## Future Improvements (FIX)

* Avoid using raw SQL statements as it makes database prone to SQL injection attacks;
* Implement monitoring for a database;
* Implement regular database backups.