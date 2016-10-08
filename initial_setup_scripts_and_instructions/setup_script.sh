#! /bin/bash
#
# I will try to get this to do all the setup that needs to happen so that
# this can be a quick and easy setup of a new bell controler.
#
#
#
#
# much of this comes from http://mjduffin.net/2015/01/03/deploying-django-gunicorn-and-nginx-on-the-raspberry-pi/
#
# at this point it assumes you are loged in as the primary admin user
#
#
#
sudo apt-get install python-virtualenv

# create user

sudo groupadd --system webapps
sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/pied-crow pied-crow
sudo mkdir -p /webapps/pied-crow/
sudo chown pied-crow /webapps/pied-crow/


# now change to the new user
sudo su - pied-crow
cd /webapps/pied-crow/
virtualenv -p /usr/bin/python3.5 .

source bin/activate

pip install django gunicorn
# may want to git clone our app repository at this point

# need to do something with a start up script for gunicorn here

source bin/deactivate

sudo aptitude install python-dev

source bin/activate
pip install setproctitle

sudo apt-get install superviser

# need to do something with the superviser pied-crow.conf file here


mkdir -p /webapps/pied-crow/logs/
touch /webapps/pied-crow/logs/gunicorn_supervisor.log



sudo supervisorctl reread
sudo supervisorctl update


sudo apt-get install nginx
sudo service nginx start


# take care of /etc/nginx/sites-available/pied-crow file here

sudo ln -s /etc/nginx/sites-available/pied-crow /etc/nginx/sites-enabled/pied-crow
sudo rm /etc/nginx/sites-enabled/default


# settings.py file
