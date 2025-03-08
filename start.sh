#!/bin/bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:api --bind 0.0.0.0:8000 &
gunicorn -w 4 -b 0.0.0.0:5000 app:app

