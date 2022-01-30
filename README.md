## Password Manager

###### What is a Password Manager?
A Password Manager is a software that allows users to store, generate, and manage their passwords for local applications and online services. 
A Password Manager assists in storing such passwords in an encrypted database.

###### Project Brief
A Password Manager written in Python using the FastAPI framework.

The exposed RESTful APIs allow Third Party Applications to easily integrate this application and utilize the complete functionalities of the Password manager.

#### Technology Stack

##### *Backend:*
Language: Python<br/>
Framework: FastAPI<br/>

##### *Database:*
Primary Database: Postgres<br/>
Cache Database: Redis

##### *Testing:*
Pytest and Locust

##### *Deployment:*
Operating System: Linux<br/>
Web-Proxy: Nginx

#### Important Modules Used in the Project:

- fastapi: FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+.
  - fastapi framework is used to build the RESTful APIs.

- Pydantic: Pydantic is a python module used for data validation. pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
  - Pydantic is used for validation of API Request Body and to define API Response Models.

- uvicorn: Uvicorn is a ASGI server implementation.<br/> 
ASGI (Asynchronous Server Gateway Interface) specify the interface and sit in between the web server and a Python web application or framework.

- SQLAlchemy: SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
  - SQLAlchemy generates the SQL statements.
  - SQLAlchemy depends on psycopg2 or other database drivers to communicate with the database.

- psycopg2: Psycopg is PostgreSQL database adapter for the Python programming language.
  - psycopg2 sends SQL statements to the database.

- alembic: Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.

- logging: This Python module defines functions and classes which implement a flexible event logging system for applications and libraries.
  - logging module will log all the application event in the `app.log` file.

- pytest: PyTest is a testing framework that allows users to write test codes using Python programming language.
  - pytest is used to write unit test as well as end to end functionality test.
  
- locust: Locust is an open source load-testing tool written in Python. It lets you write tests against your web application which mimic your user's behavior, and then run the tests at scale to help find bottlenecks or other performance issues.

### Project File Structure

```
├── README.md                                                       <- The top-level README for developers using this project
├── alembic/                                                        <- home of migration environment
│   ├── versions                                                    <- This directory holds the individual version scripts.
|   │   └── df1d9ca5f1ff_first_revision.py                          
│   ├── README                                                      <- included with the various environment templates
│   ├── env.py                                                      <- This is a Python script that is run whenever the alembic migration tool is invoked.
│   └── script.py.mako                                              <- Mako template file which is used to generate new migration scripts
├── app/
│   ├── routers
|   │   ├── accounts.py                                             <- '/accounts' endpoint functionality
|   │   ├── data.py                                                 <- '/data' endpoint functionality
|   │   ├── login.py                                                <- '/login' endpoint functionality
|   │   ├── password.py                                             <- '/password' endpoint functionality
|   │   └── users.py                                                <- '/users' endpoint functionality
│   ├── __init__.py
│   ├── config.py                                                   <- environment variables configuration file
│   ├── database.py                                                 <- database configuration file
│   ├── main.py                                                     <- main file with has the FastAPI instance
│   ├── models.py                                                   <- database table models
│   ├── oauth2.py                                                   <- authentication token based login functionality
│   ├── schemas.py                                                  <- Api request and response schema
│   └── utils.py                                                    <- Utility Functions
├── loadtest/
│   └── loadtest.py                                                 <- load test to check application's performance
├── test/
│   ├── __init__.py
│   ├── conftest.py                                                 <- pytest configuration file
│   ├── test_api.py                                                 <- endpoint testing code
│   └── test_sample.py                                              <- testing basics
├── alembic.ini                                                     <- alembic configuration file
└── requirements.txt                                                <- The requirements file for reproducing the environment
```

### Database Schema
![screenshot](https://github.com/Kartikdudeja/Backend-Application/blob/main/password_manager_database_schema.PNG)

## Quickstart

###### Prerequisites:
Be sure you have Python 3.6 or 3.6+.

###### Check Python Version
```
# check python version
python3 --version
```

###### Clone Repository and create a Virtual Environment
```
# make a new directory and clone this repository
mkdir PasswordManager/ && cd PasswordManager/
git clone https://github.com/Kartikdudeja/Backend-Application.git

# create a virtual environment
python3 -m venv <virtual_environment_name>

# install the required modules
pip3 install -r requirements.txt
```

###### Install Postgresql and Redis
[Postgresql Installation Guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

[Redis Installation Guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04)

###### Create Applicaiton Database and Tables

```
# create an application user in database
CREATE USER appuser WITH ENCRYPTED PASSWORD 'password' CREATEDB;

# create database for the application
CREATE DATABASE password_manager OWNER appuser;
```

To create table, we can use two options, one is through sqlalchemy engine, once you run the application, SQLAlchemy engine creates all the Tables specified in the `models.py` file.                                
Another way is through Alembic Migration tool

```
# run to following command to create all the tables using alembic
alembic upgrade head
```

###### Run the Application

**Note:** Before running the application, you will have to set environment variables as mentioned in `config.py` file, create a `.env` file in the Project directory and define the values.

```
# Uvicorn ASGI provides the Interface to access the application
uvicorn app.main:PassMan
```

Above command will produce the following Output:
```
INFO:     Started server process [15144]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

###### API Documentation
One of the Perks of working with FastAPI is Autmatic documentation using Swagger UI.
Swagger UI lets call and test your API directly from the browser. It presents with Interactive API documentation and exploration web user interfaces.

```
# Open this  URL in the Browser to access the Documentation
http://127.0.0.1:8000/docs
```

![screenshot](https://github.com/Kartikdudeja/Backend-Application/blob/main/Swagger_UI_Documentation.png)

###### Additional Steps

[Deamonize the Application](https://baykara.medium.com/how-to-daemonize-a-process-or-service-with-systemd-c34501e646c9)

[Setup a Proxy](https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-web-server-and-reverse-proxy-for-apache-on-one-ubuntu-18-04-server)
