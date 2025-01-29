from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import threading

app = Flask(__name__)
socketio = SocketIO(app)  # Enable WebSocket communication

# Data storage for the plot
data = []
lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_data', methods=['POST'])
def receive_data():
    global data
    try:
        value = request.get_json().get('value', None)
        if value is not None:
            with lock:
                data.append(value)
            print(f"Received value: {value}")  # Debugging log
            socketio.emit('update_plot', {'data': data})
            return jsonify({'status': 'success'})
        else:
            print("Invalid data received")  # Debugging log
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    except Exception as e:
        print(f"Error: {e}")  # Debugging log
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

