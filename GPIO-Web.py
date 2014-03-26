from flask import Flask, make_response, jsonify, url_for, request, abort
import threading
import json
import subprocess
import os
import requests
import socket
import fcntl
import struct
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. "
          "You can achieve this by using 'sudo' to run your script")

app = Flask(__name__)

gpio_mode = GPIO.BOARD
board_gpio_channels = [7, 11, 12, 13, 15, 16, 18, 22]
network_notify_url = 'http://10.0.1.49:8080/gpio'


def get_ram():
    try:
        s = subprocess.check_output(["free", "-m"])
        lines = s.split('\n')       
        return (int(lines[1].split()[1]), int(lines[2].split()[3]))
    except:
        return 0


def get_process_count():
    try:
        s = subprocess.check_output(["ps", "-e"])
        return len(s.split('\n'))
    except:
        return 0


def get_up_stats():
    try:
        s = subprocess.check_output(["uptime"])
        load_split = s.split('load average: ')
        load_five = float(load_split[1].split(',')[1])
        up = load_split[0]
        up_pos = up.rfind('','',0,len(up)-4)
        up = up[:up_pos].split('up ')[1]
        return ( up , load_five )       
    except:
        return ('', 0)


def get_connections():
    try:
        s = subprocess.check_output(["netstat","-tun"])
        return len([x for x in s.split() if x == 'ESTABLISHED'])
    except:
        return 0

def get_temperature():
    try:
        s = subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"])
        return float(s.split('=')[1][:-3])
    except:
        return 0

def get_ipaddress():
    arg='ip route list'
    p=subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    ipaddr = split_data[split_data.index('src')+1]
    return ipaddr

def get_cpu_speed():
    f = os.popen('/opt/vc/bin/vcgencmd get_config arm_freq')
    cpu = f.read()
    return cpu


def build_gpio_response(channel_list):
    gpio_info = {'gpio_mode': gpio_mode, 'pi_version': GPIO.RPI_REVISION, 'gpio_rpi_version': GPIO.VERSION, 'gpio_on': 1, 'gpio_off': 0}

    channels = []
    for channel in channel_list:
        pin = {'channel': channel, 'gpio_value': GPIO.input(channel), 'uri': url_for('set_channel_value', channel_id = channel, _external = True)}
        channels.append(pin)

    gpio_info['channels'] = channels

    return {'gpio': gpio_info}


def set_gpio_value(channel, value):
    print("Setting GPIO channel %d to value %d", channel, value)
    GPIO.output(channel, value)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': error}), 404)


@app.route('/gpio/api/v1.0/', methods=['GET'])
def get_all_channels_status():
    return jsonify(build_gpio_response(board_gpio_channels))


@app.route('/gpio/api/v1.0/<int:channel_id>', methods=['GET'])
def get_channel_status(channel_id):
    return jsonify(build_gpio_response([channel_id]))


@app.route('/gpio/api/v1.0/<int:channel_id>', methods=['POST'])
def set_channel_value(channel_id):
    if not request.json or not 'channel_value' in request.json:
        abort(400)
    set_gpio_value(channel_id, request.json['channel_value'])
    return jsonify({'message': 'ok'}), 200


def notify_network():
    
    print 'Free RAM: '+str(get_ram()[1])+' ('+str(get_ram()[0])+')'
    print 'Nr. of processes: '+str(get_process_count())
    print 'Up time: '+get_up_stats()[0]
    print 'Nr. of connections: '+str(get_connections())
    print 'Temperature in C: ' +str(get_temperature())
    print 'IP-address: '+get_ipaddress()
    print 'CPU speed: '+str(get_cpu_speed())

    data = json.dumps({'ipaddress': get_ipaddress()})
    print("Notifying GPIO Network Master of status to URL %s with data %s", network_notify_url, data)

    headers = {'content-type': 'application/json'}
    requests.post(network_notify_url, data=data, headers=headers)

    # call f() again in 60 seconds
    threading.Timer(60, notify_network).start()


if __name__ == '__main__':
    #setup GPIO using Board numbering
    GPIO.setmode(gpio_mode)

    # Sets up each pin mode
    for channel in board_gpio_channels:
        GPIO.setup(channel, GPIO.OUT, GPIO.LOW)

    # start calling notifyNetworkOfStatus now and every 60 sec thereafter
    notify_network()

    app.run(host='0.0.0.0')