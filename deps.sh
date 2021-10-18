#!/bin/bash
install-pkg libproj-dev proj-data proj-bin libgeos-dev
pip uninstall shapely -y
pip install shapely --no-binary shapely 
pip install cartopy metpy nexradaws
#python main.py