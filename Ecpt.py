import subprocess
import os

# Function to change MAC address (optional, for privacy)
def change_mac(interface):
    new_mac = "00:11:22:34:54:66"  # Randomized MAC address
    print(f"Changing MAC address of {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])

# Function to add a bridge to the torrc file
def add_bridge_to_torrc():
    bridge_ip = "1.2.3.4:443"  # Replace with your actual bridge IP
    bridge_fingerprint = "abcdef1234567890abcdef1234567890abcdef1234"  # Replace with your bridge fingerprint
    
    # Check if we have permission to modify the torrc file
    torrc_file_path = "/etc/tor/torrc"
    
    if not os.access(torrc_file_path, os.W_OK):
        print("Error: Permission denied. You need root access to modify the torrc file.")
        return
    
    try:
        with open(torrc_file_path, "a") as torrc_file:
            # Append the bridge configuration to the torrc file
            torrc_file.write(f"\nBridge obfs4 {bridge_ip} {bridge_fingerprint}\n")
            print("Bridge successfully added to the torrc file.")
    except Exception as e:
        print(f"An error occurred while adding the bridge to torrc: {e}")

# Function to restart Tor to apply new settings
def restart_tor():
    try:
        subprocess.call(["sudo", "systemctl", "restart", "tor"])
        print("Tor has been restarted to apply new bridge configurations.")
    except Exception as e:
        print(f"An error occurred while restarting Tor: {e}")

# Main function to execute the script's tasks
def main():
    # Step 1: Change the MAC address for added privacy (optional)
    interface = "eth0"  # Replace with your actual interface (e.g., wlan0)
    change_mac(interface)

    # Step 2: Add the bridge to torrc file
    add_bridge_to_torrc()

    # Step 3: Restart Tor to apply the bridge changes
    restart_tor()

    print("Now, you can manually configure additional bridges via the Tails GUI during boot-up.")
    print("Once you boot into Tails, select 'Configure Bridges' and add the second bridge.")

if __name__ == "__main__":
    main()
