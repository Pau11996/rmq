#!/bin/bash -x

while ! curl http://$POSTGRES_HOST:5432/ 2>&1 | grep '52'
do
  sleep 1
done
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
