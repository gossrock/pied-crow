#! /bin/bash
#
# I will try to get this to do all the setup that needs to happen so that
# this can be a quick and easy setup of a new bell controler.
#
#
#
#
# much of this comes from http://mjduffin.net/2015/01/03/deploying-django-gunicorn-and-nginx-on-the-raspberry-pi/
# rearranged for automation and modified for our specific application


# install all nessisary packages through apt
sudo apt-get install python-virtualenv python-dev supervisor nginx

# create user
sudo groupadd --system webapps
sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/pied-crow pied-crow
sudo mkdir -p /webapps/pied-crow/
sudo chown pied-crow /webapps/pied-crow/

# need to add the main admin user to the webapps group
# need to make sure that the prerminssions on the directories allw group read/write


# move setup some files and directories for latter
cp ./gunicorn_start /webapps/pied-crow/bin/ #gunicorn superviser startup script
mkdir -p /webapps/pied-crow/logs/ # log file directory
touch /webapps/pied-crow/logs/gunicorn_supervisor.log #log file for gunicorn
sudo cp ./pied-crow.conf /etc/supervisor/conf.d/


# enable the site
sudo cp ./pied-crow /etc/nginx/sites-available/pied-crow
sudo ln -s /etc/nginx/sites-available/pied-crow /etc/nginx/sites-enabled/pied-crow
sudo rm /etc/nginx/sites-enabled/default


# now change to the new user
sudo su - pied-crow

# create a virtualenv
virtualenv -p /usr/bin/python3 .
source bin/activate
# now install what is needed in the virtualenv
pip install django gunicorn setproctitle


# startup the supervisor
sudo supervisorctl reread
sudo supervisorctl update
# startup nginx
sudo service nginx start
