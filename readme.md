Contains various python 'services' that I have developed to run on my local Raspberry PI network.

#Installation
```
sudo apt-get install git && git clone https://github.com/jdye64/GPIO-Web.git && cd GPIO-Web && sudo ./install.sh
```

##Application Restart/Monitoring

GPIO-Web is monitored and restarted using [supervisord](#http://supervisord.org)