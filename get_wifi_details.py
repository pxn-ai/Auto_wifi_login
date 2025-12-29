import subprocess
import re

def get_connected_ssid():
    # The full path to the airport utility on macOS
    airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    
    try:
        # Run the command
        process = subprocess.run([airport_path, "-I"], capture_output=True, text=True)
        output = process.stdout
        
        # Use Regex to find ' SSID: <name>'
        match = re.search(r" SSID: (.+)", output)
        
        if match:
            return match.group(1).strip()
        else:
            return None
            
    except Exception as e:
        print(f"Error fetching SSID: {e}")
        return None

# Test it
current_ssid = get_connected_ssid()
print(f"Connected to: {current_ssid}")