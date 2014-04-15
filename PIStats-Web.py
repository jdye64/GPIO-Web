from flask import Flask, make_response, jsonify, request
import RPi_Info

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': error}), 404)


@app.route('/rpi/ram', methods=['GET'])
def set_channel_value():
    info = RPi_Info()
    print(info.get_ram())
    return make_response(jsonify({'success': 'ok'}), 200)


if __name__ == '__main__':
    app.run(port = 5001)