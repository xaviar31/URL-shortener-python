import random
import string
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# Define the static folder and URL path
app.static_folder = 'static'
app.static_url_path = '/static'

# Dictionary to map short URLs to long URLs
url_mapping = {}

# Function to generate a random short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(characters) for _ in range(5))
    return random_part

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form["long_url"]
        custom_alias = request.form["custom_alias"]

        if not long_url:
            return render_template("index.html", message="Please enter a long URL.")

        if custom_alias:
            # Check if the custom alias is already in use
            if custom_alias in url_mapping:
                return render_template("index.html", message="Alias already taken.")

            short_url = custom_alias
        else:
            # Generate a random short URL
            short_url = generate_short_url()

        # Store the mapping of short URL to long URL
        url_mapping[short_url] = long_url

        return render_template("index.html", message=f"/{short_url}")

    return render_template("index.html")

@app.route("/<alias>")
def redirect_to_original(alias):
    if alias in url_mapping:
        original_url = url_mapping[alias]
        return redirect(original_url)
    else:
        return "Alias not found.", 404

if __name__ == "__main__":
    app.run(debug=True)
