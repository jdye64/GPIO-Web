#!/bin/sh

echo 'Installing GPIO Web'
mkdir /usr/local/bin/gpiorest
chmod 755 /usr/local/bin/gpiorest
cp ./GPIO-Slave.py /usr/local/bin/gpiorest/gpioweb.py
chmod 755 /usr/local/bin/gpiorest/gpioweb.py

# Move the init script to /etc/init.d
cp ./gpio.sh /etc/init.d/gpiorest.sh
chmod 755 /etc/init.d/gpiorest.sh

echo 'Updating etc init defaults for pythonproxy'
update-rc.d gpiorest.sh defaults

echo 'GPIO Web has been installed'