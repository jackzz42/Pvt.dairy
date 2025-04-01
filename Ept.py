import os
import random
import subprocess
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import socket
import time

# Change MAC Address
def change_mac(interface):
    mac = ':'.join(['%02x' % random.randint(0, 0xFF) for _ in range(6)])
    print(f"Changing MAC address of {interface} to {mac}")
    subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', mac])

# Change Local IP Address (for example, by using a random IP in a subnet)
def change_ip():
    ip_prefix = "192.168.1."  # Adjust based on your local network subnet
    new_ip = ip_prefix + str(random.randint(100, 200))
    print(f"Changing local IP to {new_ip}")
    subprocess.call(['sudo', 'ifconfig', 'eth0', 'inet', new_ip, 'netmask', '255.255.255.0'])

# Encrypt data with AES (CBC mode, requires a 16-byte key)
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return cipher.iv + encrypted_data  # Combine IV and encrypted data for later use

# Remove Logs and Metadata
def remove_logs():
    print("Clearing system logs to remove traces...")
    log_files = ['/var/log/syslog', '/var/log/auth.log', '/var/log/kern.log']
    for log in log_files:
        try:
            with open(log, 'w') as file:
                file.truncate(0)
        except Exception as e:
            print(f"Error clearing log file {log}: {e}")

# Main function that coordinates the tasks
def main():
    # Change MAC address (you can specify the network interface name like eth0, wlan0)
    change_mac("eth0")  # Or "wlan0" for WiFi
    
    # Change Local IP Address
    change_ip()
    
    # Remove logs to clear traces
    remove_logs()
    
    # Define the encryption key
    key = hashlib.sha256("your_secret_key_here".encode()).digest()  # 256-bit key for AES
    
    # Your sensitive data that you want to send (for demonstration)
    sensitive_data = "This is a secret message"
    
    # Encrypt your data with AES before sending through the Tor network
    encrypted_data = encrypt_data(sensitive_data, key)
    
    # You can now send `encrypted_data` over Tor using the script logic (you would modify your Tor connection setup here)
    print("Encrypted data prepared to send over Tor:", encrypted_data.hex())
    
    # Run the script to start connecting to Tor (example code for connecting to Tor bridge would be placed here)
    print("Connecting to Tor...")
    time.sleep(2)  # Simulate a connection setup
    # Add your Tor connection setup here, using bridges and entry points, as needed

# Run the script
if __name__ == '__main__':
    main()
