from flask import Flask, make_response, jsonify, request

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': error}), 404)


@app.route('/gpio/api/v1.0/simulator', methods=['POST'])
def set_channel_value():
    print(request.json)
    return make_response(jsonify({'success': 'ok'}), 200)


if __name__ == '__main__':
    app.run(port = 5001)