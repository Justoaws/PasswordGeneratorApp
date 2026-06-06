from flask import Flask, render_code, request, render_template_string
import secrets
import string

app = Flask(__name__)

# Core logic (same as before)
def generate_secure_password(length=16):
    if length < 8: length = 8
    letters_lower = string.ascii_lowercase
    letters_upper = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*()-_=+"
    
    all_characters = letters_lower + letters_upper + digits + special_chars
    password = [
        secrets.choice(letters_lower),
        secrets.choice(letters_upper),
        secrets.choice(digits),
        secrets.choice(special_chars)
    ]
    password += [secrets.choice(all_characters) for _ in range(length - 4)]
    secrets.SystemRandom().shuffle(password)
    return "".join(password)

# HTML Template rendered in the browser
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Password Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f4f4f9; text-align: center; }
        .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }
        input[type="number"] { padding: 10px; width: 60px; font-size: 16px; }
        button { padding: 10px 20px; font-size: 16px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .result { margin-top: 20px; font-size: 20px; font-weight: bold; color: #28a745; background: #e2f0d9; padding: 10px; border-radius: 5px; word-break: break-all; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Enterprise Password Generator</h2>
        <form method="POST">
            <label>Password Length: </label>
            <input type="number" name="length" value="{{ length }}" min="8" max="64">
            <button type="submit">Generate</button>
        </form>
        {% if password %}
            <div class="result">
                <strong>Your Password:</strong> <code style="color: #d63384;">{{ password }}</code>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    password = ""
    length = 16
    if request.method == "POST":
        try:
            length = int(request.form.get("length", 16))
        except ValueError:
            length = 16
        password = generate_secure_password(length)
    
    return render_template_string(HTML_TEMPLATE, password=password, length=length)

if __name__ == "__main__":
    # Host 0.0.0.0 makes the server accessible from outside the EC2 instance
    # Port 5000 is the default web port for Flask
    app.run(host="0.0.0.0", port=5000)
