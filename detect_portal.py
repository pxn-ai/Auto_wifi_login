import urllib.request
import ssl

def check_network_state():
    # Apple's test URL
    test_url = "http://captive.apple.com/hotspot-detect.html"
    
    try:
        # Ignore SSL errors (standard for captive portals)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        # Fake a browser User-Agent (some networks block Python scripts)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        req = urllib.request.Request(test_url, headers=headers)
        
        # Custom opener to track redirects
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        response = opener.open(req, timeout=5)
        
        # Read content
        raw_content = response.read().decode('utf-8')
        final_url = response.geturl()

        # Debugging: Show us exactly what we got!
        print(f"DEBUG: Final URL: {final_url}")
        print(f"DEBUG: Content received: '{raw_content.strip()}'")

        # LOOSE CHECK: If the URL is still Apple's AND "Success" is in the text -> Online
        if "captive.apple.com" in final_url and "Success" in raw_content:
            return "ONLINE", final_url
            
        # If URL changed OR "Success" is missing -> Captive
        else:
            return "LOGIN_NEEDED", final_url

    except Exception as e:
        print(f"Error: {e}")
        return "OFFLINE", None

# --- TEST ---
status, url = check_network_state()

if status == "ONLINE":
    print("✅ Status: ONLINE (No login needed)")
elif status == "LOGIN_NEEDED":
    print(f"⚠️ Status: CAPTIVE PORTAL DETECTED")
    print(f"   Target Login Page: {url}")
else:
    print("❌ Status: OFFLINE")