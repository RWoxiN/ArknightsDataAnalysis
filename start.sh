#!/bin/bash

vardate=$(date +%c)
source ./venv/bin/activate
python main.py && echo "${vardate}: runing succeed!" >> ./start.log 2>&1