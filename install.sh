#!/bin/sh

#Install python development tools
sudo apt-get -y install python-dev python-setuptools
wget http://python-distribute.org/distribute_setup.py
sudo python distribute_setup.py
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
sudo python get-pip.py
sudo pip install virtualenv virtualenvwrapper

#Removing installation scripts
rm distribute-0.6.49.tar.gz
rm distribute_setup.py
rm get-pip.py

echo 'Creates the GPIO project'
mkdir gpio
cd gpio
virtualenv gpio-web
. gpio-web/bin/activate

echo 'Installing GPIO project python dependencies'
pip install rpi.gpio
pip install flask
pip install peewee

echo "Installing Git"
sudo apt-get -y install git

echo 'Downloading GPIO-Web project from jdye64'
git clone https://github.com/jdye64/GPIO-Web.git

echo 'Install NGinx'
sudo apt-get -y install nginx

echo 'Installing Gunicorn'
sudo apt-get -y install gunicorn

echo 'Installing Supervisor"
sudo apt-get -y install supervisor




#echo 'Installing GPIO Web'
#mkdir /usr/local/bin/gpiorest
#chmod 755 /usr/local/bin/gpiorest
#cp ./GPIO-Slave.py /usr/local/bin/gpiorest/gpioweb.py
#chmod 755 /usr/local/bin/gpiorest/gpioweb.py

# Move the init script to /etc/init.d
#cp ./gpio.sh /etc/init.d/gpiorest.sh
#chmod 755 /etc/init.d/gpiorest.sh

#echo 'Updating etc init defaults for pythonproxy'
#update-rc.d gpiorest.sh defaults

#echo 'GPIO Web has been installed'