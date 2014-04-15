from flask import Flask, make_response, jsonify, url_for, request, abort
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. "
          "You can achieve this by using 'sudo' to run your script")

app = Flask(__name__)

gpio_mode = GPIO.BOARD
board_gpio_channels = [7, 11, 12, 13, 15, 16, 18, 22]


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


if __name__ == '__main__':
    #setup GPIO using Board numbering
    GPIO.setmode(gpio_mode)

    # Sets up each pin mode
    for channel in board_gpio_channels:
        GPIO.setup(channel, GPIO.OUT, GPIO.LOW)

    app.run(host='0.0.0.0')