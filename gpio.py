from flask import Flask, make_response, jsonify

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges."
          "You can achieve this by using 'sudo' to run your script")

gpio_mode = GPIO.BOARD
GPIO_OFF = True
GPIO_ON = False
board_gpio_channels = [3, 5, 7, 8, 10, 11, 12, 13]
outlet_to_gpio_mapping = {"A": 5, "B": 8, "C": 11, "D": 13, "E": 3, "F": 7, "G": 10, "H": 12}

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': error}), 404)

@app.route('/gpio/on/<out_id>', methods=['GET'])
def turn_on_outlet(out_id):
    print "Turning on outlet: " + out_id
    GPIO.output(outlet_to_gpio_mapping[out_id], GPIO_ON)
    return "OK"

@app.route('/gpio/off/<out_id>', methods=['GET'])
def turn_off_outlet(out_id):
    print "Turning off outlet: " + out_id
    GPIO.output(outlet_to_gpio_mapping[out_id], GPIO_OFF)
    return "OK"


if __name__ == '__main__':

    print "Setting up GPIO support"
    GPIO.setmode(gpio_mode)
    for channel in board_gpio_channels:
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO_OFF)
    print "GPIO support has been enabled"

    app.config['DEBUG'] = True
    app.run(host='0.0.0.0')
