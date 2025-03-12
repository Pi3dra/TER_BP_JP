import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def process_data(data):
    received_time = time.time()
    sent_time = data['timestamp']
    latency = temps_reception - temps_envoie
    print(f"Received value: {data['value']} | latency: {latency:.4f} seconds")
    #Ici appeler une autre fonction pour controller la voiture

sio.connect("http://192.168.2.2/")

while True
    time.sleep(1)
