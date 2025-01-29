import requests
import random
import time

# Set the server IP address and port
server_ip = "http://192.168.248.26:5000/send_data"  # Replace <PC_IP_ADDRESS> with your PC's IP address

# Function to send random integers to the server
def send_data():
    while True:
        # Generate a random integer between 0 and 15
        random_integer = random.randint(0, 15)

        # Create the data payload
        data_to_send = {"value": random_integer}

        # Send the data to the server
        try:
            response = requests.post(server_ip, json=data_to_send)
            if response.status_code == 200:
                print("Sent:", random_integer)
            else:
                print("Failed to send data. Status code:", response.status_code)
        except Exception as e:
            print(f"Error sending data: {e}")

        # Wait for 1 second before sending the next value
        time.sleep(1)

if __name__ == "__main__":
    send_data()

