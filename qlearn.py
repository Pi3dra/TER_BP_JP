import time
import numpy as np
import socketio
import RPi.GPIO as GPIO
import os
import sys
import argparse
import select
import tty
import termios

# =================== CONFIGURATION ===================
MOTOR_PIN = 18       # Broche GPIO utilisée pour le PWM
PWM_FREQUENCY = 800  # Fréquence du PWM en Hz


# Actions possibles pour l'agent Q-learning
actions = ["DO_NOTHING", "INCREASE_POWER", "DECREASE_POWER" ] 

# Discrétisation de l'espace d'états (par exemple 15 états pour 0 à 14 V)
num_states = int(14.7 / 0.75) + 1
# Initialisation de la Q-table (num_states x nombre d'actions)
q_table = np.zeros((num_states, len(actions)), dtype=float)

# Hyperparamètres du Q-learning
learning_rate = 0.3       # alpha
discount_factor = 0.9     # gamma
epsilon = 0.3             # taux d'exploration (epsilon-greedy)

# Paramètres de contrôle du moteur
max_speed = 95
min_speed = 0
speed_step = 1
big_speed_step = 2
current_speed = 0    

# Initialisation du client Socket.IO
sio = socketio.Client()

prev_state = None
prev_action = None

# Q-table file for saving/loading
Q_TABLE_FILE = "q_table.npy"

# =================== Q-table Loading ===================
def load_q_table(file_path):
    """
    charge une Q-table depuis un fichier 
    """
    global q_table
    try:
        if os.path.exists(file_path):
            loaded_table = np.load(file_path)
            if loaded_table.shape == q_table.shape:
                q_table = loaded_table
                print(f"[Q-Learning] Q-table chargé depuis {file_path}")
            else:
                print(f"[Q-Learning] Warning: Q-Table {loaded_table.shape} "
                      f"n'a pas la meme forme que {q_table.shape}.")
        else:
            print(f"[Q-Learning] pas de Q-table a {file_path}.")
    except Exception as e:
        print(f"[Q-Learning] Erreur en chargeant la Q-table a {file_path}: {e}.")

# =================== Q-table Saving ===================
def save_q_table():
    """
    enregistre la q-table courante
    """
    try:
        np.save(Q_TABLE_FILE, q_table)
        print(f"[Q-Learning] Q-table saved to {Q_TABLE_FILE}")
    except Exception as e:
        print(f"[Q-Learning] Error saving Q-table: {e}")

def is_data():
    """
    ceci permet de lire input du terminal sans arreter le programmer
    """
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def check_spacebar():
    """
    on regarde si on presse la barre espace pour enregistrer
    """
    if is_data():
        c = sys.stdin.read(1)
        if c == ' ':
            save_q_table()
            return True
    return False

# =================== Fonctions utilitaires ===================
def get_state(voltage):
    """
    Convertir la tension lue en un état discret.
    """
    scaled = int(voltage / 0.75)  
    return min(scaled, num_states - 1)

def choose_action(state):
    if np.random.rand() < epsilon:
        return np.random.choice(len(actions))  # Exploration
    else:
        return np.argmax(q_table[state])      # Exploitation

def update_q_table(state, action, reward, next_state):
    """
    Met à jour la Q-table en utilisant la formule de Bellman.
    """
    best_next_action = np.argmax(q_table[next_state])
    q_table[state, action] += learning_rate * (
        reward + discount_factor * q_table[next_state, best_next_action]
        - q_table[state, action]
    )

def compute_reward(voltage, action):
    """
    Calcule la récompense en fonction de la tension reçue.
    """
    global current_speed
    if voltage >= 14.0:
        if action == "DECREASE_POWER":
            print(action)
            return 100
        return -250
    if voltage < 1.40:
        if action == "INCREASE_POWER":
            return 20
        return -20
    else:
        return abs(20.0 * (voltage / 14.5))

def apply_action(action_idx, pwm):
    """
    Applique l'action choisie en ajustant la vitesse via PWM.
    """
    global current_speed
    action_name = actions[action_idx]

    if action_name == "INCREASE_POWER":
        current_speed += speed_step
    elif action_name == "DECREASE_POWER":
        current_speed -= speed_step
    elif action_name == "DO_NOTHING":
        pass

    # Borne la valeur du duty cycle
    current_speed = max(min_speed, min(max_speed, current_speed))
    pwm.ChangeDutyCycle(current_speed)
    print(f"[apply_action] Action: {action_name}, Vitesse => {current_speed}%")

# =================== Gestion des événements Socket.IO ===================
@sio.event
def connect():
    print("[Q-Learning] Connecté au serveur.")

@sio.event
def disconnect():
    print("[Q-Learning] Déconnecté du serveur.")

def print_q_table(q_table):
    os.system("clear")  # Clear terminal (use "cls" on Windows)
    print("Q-TABLE :")
    print("-" * 50)
    print(f"{'State':<8} {'DO_NOTHING':<12} {'INCREASE_POWER':<15} {'DECREASE_POWER':<15}")
    print("-" * 50)
    for state in range(q_table.shape[0]):
        print(f"{state:<8} {q_table[state,0]:<12.2f} {q_table[state,1]:<15.2f} {q_table[state,2]:<15.2f}"  )
    print("-" * 50)

@sio.on('update_plot')
def on_update_plot(data):
    try:
        global current_speed, prev_state, prev_action
        voltage = float(data['value'])
        state = get_state(voltage)
        action_idx = choose_action(state)
        reward = compute_reward(voltage, actions[action_idx])
        next_state = state

        if prev_state is not None and prev_action is not None:
            update_q_table(prev_state, prev_action, reward, state)

        apply_action(action_idx, pwm)

        prev_state = state
        prev_action = action_idx

        print_q_table(q_table)

    except Exception as e:
        print(f"Erreur dans on_update_plot: {e}")

# =================== Programme principal ===================
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Q-learning avec enregistrement de la q-table")
    parser.add_argument('--qtable', type=str, default=None, help="Chemin vers Q-table")
    parser.add_argument('--ip', type=str, required=True, help="IP address of the Flask server")
    args = parser.parse_args()

    # Construct SERVER_URL from provided IP
    SERVER_URL = f"http://{args.ip}:5000"

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())

        if args.qtable:
            load_q_table(args.qtable)

        # Initialisation du GPIO et du PWM
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOTOR_PIN, GPIO.OUT)
        pwm = GPIO.PWM(MOTOR_PIN, PWM_FREQUENCY)
        pwm.start(0)

        # Se connecter au serveur Socket.IO
        sio.connect(SERVER_URL)
        print("[Q-Learning] En attente des données...")

        # check pour la barre space 
        while True:
            check_spacebar()
            time.sleep(0.01)  

    except KeyboardInterrupt:
        print("[Q-Learning] Interrompu par l'utilisateur.")
        save_q_table()  # Save Q-table on exit
    except Exception as e:
        print(f"[Q-Learning] Erreur: {e}")
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        pwm.stop()
        GPIO.cleanup()
        sio.disconnect()
