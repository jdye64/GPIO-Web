from flask import Flask, make_response, jsonify
# import RPi.GPIO as GPIO
import threading

app = Flask(__name__)


pins = [
    {
        'gpio_version': 'Rev2',
        'wiringPi': 0,
        'GPIO': 17,
        'Phys': 11,
        'Name': 'GPIO 0',
        'Mode': 'IN',
        'Value': 'HIGH'
    },
    {
        'gpio_version': 'Rev2',
        'wiringPi': 1,
        'GPIO': 18,
        'Phys': 12,
        'Name': 'GPIO 1',
        'Mode': 'IN',
        'Value': 'OUT'
    }
]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': error}), 404)


@app.route('/gpio/api/v1.0/pins', methods=['GET'])
def get_all_pins_status():
    return jsonify({'gpio_all': pins})


@app.route('/gpio/api/v1.0/pin/<int:task_id>', methods=['GET'])
def get_pin_status():
    return jsonify({'gpio_all': pins})


@app.route('/')
def hello_world():
    return 'Hello World!'


def notify_network():
    print("Notifying GPIO Network Master of status")
    # call f() again in 60 seconds
    threading.Timer(60, notify_network).start()


if __name__ == '__main__':
    #setup GPIO using Board numbering
    GPIO.setmode(GPIO.BOARD)

    # start calling notifyNetworkOfStatus now and every 60 sec thereafter
    notify_network()

    app.run()


# def getmac(interface):
#   # Return the MAC address of interface
#   try:
#     str = open('/sys/class/net/%s/address', %interface).readline()
#   except:
#     str = "00:00:00:00:00:00"
#   return str[0:17]
