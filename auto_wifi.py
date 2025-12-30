import urllib.request
import urllib.parse
import ssl
import time

# --- CONFIGURATION ---
KNOWN_NETWORKS = {
    "Test_Lab_Pi": {
        # TRIGGER: We now look for specific TEXT on the page, not just the URL
        "trigger_content": "Lord of the Pings", 
        
        "type": "POST",
        "username": "TestUser123",
        "password": "MySecretPassword",
        "user_field": "student_id",      
        "pass_field": "student_pass"
    },
    "University_Network": {
        # You can still use URL matching for the real uni
        "trigger_url": "moratuwa.ac.lk",
        
        "type": "POST",
        "username": "YOUR_REAL_ID",
        "password": "YOUR_REAL_PASS",
        "user_field": "auth_user",      
        "pass_field": "auth_pass"
    }
}

def check_network_state():
    test_url = "http://captive.apple.com/hotspot-detect.html"
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        
        req = urllib.request.Request(test_url, headers=headers)
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        response = opener.open(req, timeout=5)
        
        raw_content = response.read().decode('utf-8')
        final_url = response.geturl()

        # Debug print to help you see what the script sees
        # print(f"DEBUG: URL={final_url} | Content-Snippet={raw_content[:50]}")

        if "captive.apple.com" in final_url and "Success" in raw_content:
            return "ONLINE", final_url, raw_content
        else:
            return "CAPTIVE", final_url, raw_content

    except Exception as e:
        return "OFFLINE", str(e), ""

def login_to_network(url, config):
    print(f"   >> Initiating Login Sequence...")
    
    data = {
        config["user_field"]: config["username"],
        config["pass_field"]: config["password"]
    }
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    
    try:
        # Note: In a real redirect scenario, we post to the redirected URL.
        # In our Pi scenario, we post to the URL we are currently on.
        req = urllib.request.Request(url, data=encoded_data, method="POST")
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        response = urllib.request.urlopen(req, context=ctx)
        print("   >> Credentials Sent! verifying connection...")
        time.sleep(2)
        
        status, _, _ = check_network_state()
        if status == "ONLINE":
            print("   ✅ LOGIN SUCCESSFUL!")
        else:
            print("   ❌ Login failed. The portal might have rejected the credentials.")
            
    except Exception as e:
        print(f"   ❌ Error during login POST: {e}")

# --- MAIN LOOP ---
print("--- Wi-Fi Auto Login V2 Started ---")

# Run once immediately
status, url, content = check_network_state()

if status == "ONLINE":
    print("✅ Online. (No action needed)")
    
elif status == "CAPTIVE":
    print(f"⚠️ Captive Portal Detected.")
    print(f"   URL: {url}")
    
    network_found = False
    for net_name, config in KNOWN_NETWORKS.items():
        # Check 1: Does the URL match?
        url_match = "trigger_url" in config and config["trigger_url"] in url
        
        # Check 2: Does the HTML Content match?
        content_match = "trigger_content" in config and config["trigger_content"] in content
        
        if url_match or content_match:
            print(f"   >> Identified Network: {net_name}")
            login_to_network(url, config)
            network_found = True
            break
    
    if not network_found:
        print("   >> Unknown Network. No matching config found.")
        print("   >> Tip: Check the HTML content for unique words to add to 'trigger_content'.")

else:
    print(f"❌ Offline. Error: {url}")