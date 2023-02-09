#!/bin/bash
ps -ef|grep gunicorn|grep -v grep|awk '{print $2}'
if [ -n "$pid"]
then
    echo "kill -9 pid:" $pid
    kill -9 $pid
fi
git pull
nohup gunicorn main:app --bind 0.0.0.0:8080 --worker-class uvicorn.workers.UvicornWorker --timeout 0