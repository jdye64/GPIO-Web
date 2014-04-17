#!/bin/sh

echo 'Installing GPIO Web'
mkdir /usr/local/bin/gpio
chmod 755 /usr/local/bin/gpio
cp ./GPIO-Web.py.py /usr/local/bin/gpio/.
chmod 755 /usr/local/bin/gpio/GPIO-Web.py

# Move the init script to /etc/init.d
cp ./gpio.sh /etc/init.d/.
chmod 755 /etc/init.d/gpio.sh

echo 'Updating etc init defaults for pythonproxy'
update-rc.d gpio.sh defaults

echo 'GPIO Web has been installed'