import requests
import random
import time

# IMPORTANT: CHANGER L'IP ET LE PORT !
server_ip = "http://192.168.248.26:5000/send_data"  

def send_data():
    while True:
        randint = random.randint(0, 15)
        donnees = {"value": randint}

        #Envoie les données au serveur 
        try:
            #techniquement ce n'est pas necessaire d'attendre une reponse du serveur quand on envoie a travers POST 
            #ceci, mais c'est pratique pour debug
            reponse = requests.post(server_ip, json = donnees)
            if reponse.status_code == 200:
                print("Envoyée:", randint)
            else:
                print("Erreur de transmission:. Status code:", reponse.status_code)

        except Exception as e:
            print(f"Erreur de transmission: {e}")

        time.sleep(1)

#Cela empeche de executer send_data immediatement si le script est importé ailleurs
#Cela sera utile quand on voudra envoyer et executers des instructions en fonctions des instructions du Q-Learning
if __name__ == "__main__":
    send_data()

