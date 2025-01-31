from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import threading

app = Flask(__name__)

#Activation du serveur SocketIO
socketio = SocketIO(app)

#Données 
data = []
lock = threading.Lock()

#Graphique
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_data', methods=['POST'])
def receive_data():
    '''
    Cette fonction prend en charge la reception des données et la mise a jour du graphique
    Elle est appellée apres la reception des donnees au chemin /send_data a travers la methode
    HTTP POST, elle ajoute les donnees reçues puis emet un signal 'update_plot' qui est ensuite
    reçu par le frontend html qui met a jour le graphique
    '''
    global data
    try:
        value = request.get_json().get('value', None)
        if value is not None:
            with lock:
                data.append(value)
            print(f"Donnée reçue: {value}")  # Debug
            socketio.emit('update_plot', {'data': data})
            return jsonify({'status': 'success'})
        else:
            print("Donnée Invalide")  # Debug
            return jsonify({'status': 'error', 'message': 'Donnée Invalide'}), 400

    except Exception as e:
        print(f"Error: {e}")  
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000) #, debug = true)

