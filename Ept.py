import os
import random
import subprocess
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from PIL import Image

# Function to change the MAC address
def change_mac(interface):
    new_mac = ":".join(["{:02x}".format(random.randint(0, 255)) for _ in range(6)])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    print(f"MAC address of {interface} changed to {new_mac}")

# Function to generate a new AES encryption key (256-bit)
def generate_encryption_key():
    return os.urandom(32)  # 256-bit key for AES-256

# Function to encrypt data using AES encryption
def encrypt_data(data, key):
    iv = os.urandom(16)  # Initialization Vector (IV) for AES
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad data to make it a multiple of 16 bytes (for AES)
    padding_length = 16 - len(data) % 16
    padded_data = data + chr(padding_length) * padding_length
    encrypted_data = encryptor.update(padded_data.encode()) + encryptor.finalize()

    # Return base64 encoded encrypted data (iv + encrypted data)
    return base64.b64encode(iv + encrypted_data).decode()

# Function to remove EXIF data from an image
def remove_exif(image_path):
    try:
        image = Image.open(image_path)
        data = list(image.getdata())  # Get the image data without EXIF
        image_no_exif = Image.new(image.mode, image.size)
        image_no_exif.putdata(data)
        image_no_exif.save(image_path)
        print(f"EXIF data removed from {image_path}")
    except Exception as e:
        print(f"Error removing EXIF data from {image_path}: {e}")

# Function to clear system logs (e.g., bash history, system logs)
def clear_logs():
    logs_to_clear = [
        "/root/.bash_history",  # Root bash history
        "/home/user/.bash_history",  # User bash history
        "/var/log/*",  # System logs
    ]
    
    for log in logs_to_clear:
        subprocess.call(["sudo", "rm", "-f", log])  # Remove logs
    print("System logs and history cleared.")

# Main function to execute all tasks
def main():
    # Step 1: Change the MAC address
    interface = "eth0"  # or "wlan0" for Wi-Fi, modify if necessary
    change_mac(interface)

    # Step 2: Generate a new encryption key
    key = generate_encryption_key()
    print(f"New encryption key generated: {base64.b64encode(key).decode()}")

    # Step 3: Encrypt some data using the new encryption key
    data = "Sensitive data that needs encryption."
    encrypted_data = encrypt_data(data, key)
    print(f"Encrypted data: {encrypted_data}")

    # Step 4: Clear logs and history
    clear_logs()

    # Step 5: Remove EXIF data from an image (if applicable)
    image_path = "/path/to/your/image.jpg"  # Update with the actual path to your image
    remove_exif(image_path)

if __name__ == "__main__":
    main()
