# Weather Collector simple app for horHeat project

### This project will be used  to save weather conditions into postgresql database ###

    Technology:
        - sqlacodegen (app for grabbing structure of db) exampl: sqlacodegen postgresql://<example_user>:<example_password>@<example_ip:port>/<example_db_name> > outputs_files.py
        - SqlAlchemy (ORM), to working with db, based on db structure from sqlacodegen ^^
        - requests (for grabbing data from weather api)

## How to start

Go to code directory

```sh
$ cd weather_collector
```

Make virtualenv

```sh
$ virtualenv venv --python=python3
```

Source venv

```sh
$ . venv/bin/activate
```

Install requirements

```sh
$ pip install -r requirements.txt
```


### Set DB and Weather Api settings
In app directory create private_config.py file with parameters:

```
remote_db = 'postgresql://<user>:<password>@<ip:port>/<db_name>'
apikey = '<apikey_from_weatherbitio_website>'
```

or similiar export to os
```
export DATABASE_REMOTE_URL="postgresql://<user>:<password>@<ip:port>/<db_name>"
export WEATHERBIT_API_KEY="<apikey_from_weatherbitio_website>"
```

## How to run

To grabb current_weather from cities you need to:

```sh
$ python app/current_weather_collector.py
```

If you want to see last 50 records from db:

```sh
$ python app/check_weather_tables.py
```

Simplest way for scheduling:
https://askubuntu.com/questions/799023/how-to-set-up-a-cron-job-to-run-every-10-minutes
