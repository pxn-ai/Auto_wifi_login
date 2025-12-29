import urllib.request
import ssl

def check_network_state():
    # Apple's official endpoint for checking Wi-Fi login status
    # It returns exactly one word: "Success" if you are online.
    test_url = "http://captive.apple.com/hotspot-detect.html"
    
    try:
        # Create a context that ignores SSL errors (captive portals often have bad certs)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Attempt to open the URL
        req = urllib.request.Request(test_url)
        
        # We use a custom opener to catch the redirect URL
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        response = opener.open(req, timeout=5)
        
        # Read the content
        content = response.read().decode('utf-8').strip()
        final_url = response.geturl()

        if content == "Success":
            print("✅ Status: ONLINE (Already logged in)")
            return "ONLINE", final_url
        else:
            # If content isn't "Success", we are likely at a login page
            print(f"⚠️ Status: CAPTIVE PORTAL DETECTED")
            print(f"Redirected to: {final_url}")
            return "LOGIN_NEEDED", final_url

    except Exception as e:
        print(f"❌ Status: OFFLINE (Wi-Fi might be off or disconnected)")
        print(f"Error: {e}")
        return "OFFLINE", None

# --- AUTOMATION LOGIC ---
status, login_url = check_network_state()

if status == "LOGIN_NEEDED":
    # IDENTIFY THE NETWORK BASED ON THE URL
    
    if "moratuwa.ac.lk" in login_url or "10.10." in login_url:
        print(">> Detected University Network. Initiating Uni Login...")
        # Run your Uni login function here
        
    elif "starbucks" in login_url:
        print(">> Detected Starbucks. Clicking Accept...")
        
    else:
        print(f">> Unknown Login Page: {login_url}")