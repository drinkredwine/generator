#!/usr/bin/env bash

echo generate data
~/.virtualenvs/py35/bin/python main.py
echo copy data
scp data/*.csv jkovac@exponea.com:/usr/share/nginx/demo-data.exponea