import subprocess
import re

def get_wifi_scutil():
    # We pipe commands into scutil to read the AirPort (Wi-Fi) state dictionary
    cmd = "printf 'get State:/Network/Interface/en0/AirPort\\nd.show\\n' | scutil"
    
    try:
        # shell=True is required here to handle the pipe (|)
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = process.stdout
        
        # We are looking for the key "SSID_STR"
        match = re.search(r'\s+SSID_STR : (.+)', output)
        
        if match:
            return match.group(1).strip()
        else:
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

# Run it
ssid = get_wifi_scutil()
if ssid:
    print(f"Connected to: {ssid}")
else:
    print("Could not retrieve SSID. Permissions might be fully blocked.")