#!/bin/bash

export PG_HOST=127.0.0.1
export PG_PORT=38734
export PG_USER=project
export PG_PASSWORD=project
export PG_DBNAME=project_db
export SECRET_KEY=django-insecure-%=yxp#$#*txi-li*d@=pl5t5415p5_9hm3ram2lioqx**h&m0
python3.11 manage.py test $1