#!/bin/bash

set -e

sudo docker-compose up -d
echo "ждем 30 sek контейнет запускается "
sleep 30

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

pip install -r requirements.txt

python baza.py

python main.py
