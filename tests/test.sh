#!/bin/bash

export PG_HOST=localhost
export PG_PORT=5432
export PG_USER=project
export PG_PASSWORD=project
export PG_DBNAME=project_db
export SECRET_KEY=ju7t_my_7ecret%_key_4django
python3.11 manage.py test $1