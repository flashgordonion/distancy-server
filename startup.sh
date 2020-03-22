#!/bin/bash

echo Starting Distancy Server.

exec gunicorn \
  --bind 0.0.0.0:8000 \
  --workers 6 \
  --capture-output \
  --chdir /user/app/src/ distancy_server.wsgi:application
