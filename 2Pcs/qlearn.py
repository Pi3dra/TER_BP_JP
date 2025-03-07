'''
Q-learning est une Q-table qui sauvegarde la valeur stimeé de prendre chaque action
dans un etat s

Chaque cellule Q(s,a) represente la recompensée attendue de faire l'action a dans l'etat s


la formule est:

(Equation de Bellman)

    Q(s,a) = Q(s,a) + alpha*[R + gamma*(max-a'Q(s',a')) - Q(s,a)]

Q(s,a) = Q-value qu'on connait

R = recompense apres avoir pris l'action

s' = Etat apres avoir fait l'action a

max-a'Q(s',a') = le Q-value plus grand de l'etat suivant

alpha = learning rate, a quel point la nouvelle info ecrasse la precedente

gamma = Discount factor, a quel point on pense a long-terme



L'idee est la suivante

creer un tableau pour chaque paire etat-action

ex:
    etat accelerer decelerer continuer


l'agent prend une action random avec probabilité epsilon, et il prend l'action
avec le meilleur Q-value avec une probabilité 1-epsilon

l'agetn fait l'action et il reçoit un nouveau etat et une recompense R

en utilisant la formule on met a jour Q(s,a)

continuer jusqu'a la convergence


'''

import socketio
import time
import numpy as np

SERVER_URL = "http://YOUR_PI_1_IP:5000"  # Replace with the IP of Raspberry Pi 1

sio = socketio.Client()

# Q-learning setup
actions = ["DO NOTHING", "INCREASE POWER", "DECREASE POWER"]
q_table = np.zeros((10, len(actions)))  # 10 voltage states, 3 actions
learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.2  # Exploration rate

def get_state(voltage):
    """Convert voltage into a discrete state (0-9)."""
    return min(int(voltage * 2), 9)  # Example: Scale 0-5V to 0-9 states

def choose_action(state):
    """Epsilon-greedy action selection."""
    if np.random.rand() < epsilon:
        return np.random.choice(len(actions))  # Explore
    return np.argmax(q_table[state])  # Exploit

def update_q_table(state, action, reward, next_state):
    """Q-learning update rule."""
    best_next_action = np.argmax(q_table[next_state])
    q_table[state, action] += learning_rate * (reward + discount_factor * q_table[next_state, best_next_action] - q_table[state, action])

@sio.event
def connect():
    print("Connected to server")

@sio.on('update_plot')
def on_message(data):
    latest_data = data['data'][-1]
    voltage = latest_data['value']
    sent_timestamp = latest_data['timestamp']
    
    received_timestamp = time.time()
    delay = received_timestamp - sent_timestamp
    print(f"Received voltage: {voltage}, Delay: {delay:.6f} sec")

    state = get_state(voltage)
    action = choose_action(state)

    # Define rewards (example: want voltage between 2.5V-3.5V)
    if 2.5 <= voltage <= 3.5:
        reward = 1  # Ideal range
    else:
        reward = -1  # Out of range

    next_state = get_state(voltage)  # Assuming environment transition
    update_q_table(state, action, reward, next_state)

    print(f"Action taken: {actions[action]}, New Q-table: \n{q_table}")

#Faut s'adapter pour faire 
sio.connect(SERVER_URL)
sio.wait()

