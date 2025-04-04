from flask import Flask, render_template, request, jsonify, session
from captcha.image import ImageCaptcha
import random
import string
import io
import base64

app = Flask(__name__)
app.secret_key = "your_secret_key"

def generate_captcha_text():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))

def generate_captcha():
    captcha_text = generate_captcha_text()
    session["captcha_text"] = captcha_text  

    image = ImageCaptcha()
    image_data = image.generate(captcha_text)
    image_bytes = io.BytesIO(image_data.getvalue())  
    captcha_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")  

    return captcha_base64, captcha_text

@app.route("/")
def index():
    captcha_image, captcha_text = generate_captcha()
    return render_template("login.html", captcha_image=captcha_image, captcha_text=captcha_text)

@app.route("/reload_captcha")
def reload_captcha():
    captcha_image, captcha_text = generate_captcha()
    return jsonify({"captcha_image": captcha_image, "captcha_text": captcha_text})

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    entered_captcha = request.form.get("captcha")

    valid_username = "kaveen"
    valid_password = "kaveen123"

    if username == valid_username and password == valid_password and entered_captcha == session.get("captcha_text", ""):
        return jsonify({"success": True, "message": "Login Successfully"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})

if __name__ == "__main__":
    app.run(debug=True)
