import subprocess
import re

def get_wifi_scutil():
    # Use scutil with stdin to avoid shell=True security risk
    scutil_input = "get State:/Network/Interface/en0/AirPort\nd.show\n"
    
    try:
        # SECURITY: Avoid shell=True by piping input directly to subprocess
        process = subprocess.run(
            ["scutil"],
            input=scutil_input,
            capture_output=True,
            text=True
        )
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