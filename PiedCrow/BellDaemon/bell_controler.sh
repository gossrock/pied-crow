#! /bin/bash

source /webapps/pied-crow/bin/activate
export PYTHONPATH='/webapps/pied-crow/pied-crow/PiedCrow/'
python3 /webapps/pied-crow/pied-crow/PiedCrow/BellDaemon/bell_controler.py
