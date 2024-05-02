#To run this code:

#Save it to a file named app.py.
#Make sure you have Flask installed (pip install flask).
#Run python app.py.
#Access the application at http://localhost:5000.

from flask import Flask, request, redirect, render_template_string
import sqlite3
import string
import random

app = Flask(__name__)

# Function to generate a random shortcode
def generate_shortcode():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

# Function to create a shortened URL entry in the database
def create_shortened_url(original_url):
    shortcode = generate_shortcode()
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("INSERT INTO urls (original_url, shortcode) VALUES (?, ?)", (original_url, shortcode))
    conn.commit()
    conn.close()
    return shortcode

# Function to retrieve the original URL from the database
def get_original_url(shortcode):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute("SELECT original_url FROM urls WHERE shortcode=?", (shortcode,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

# Homepage
@app.route('/')
def index():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>URL Shortener</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container mt-5">
                <h1 class="mb-4">URL Shortener</h1>
                <form action="/shorten" method="post">
                    <div class="form-group">
                        <input type="url" class="form-control" name="url" placeholder="Enter URL to shorten" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Shorten</button>
                </form>
            </div>
        </body>
        </html>
    """)

# Shorten URL endpoint
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    shortcode = create_shortened_url(original_url)
    short_url = request.host_url + shortcode
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>URL Shortener</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container mt-5">
                <h1 class="mb-4">URL Shortened Successfully</h1>
                <p class="lead">Shortened URL:</p>
                <a href="{{ short_url }}" target="_blank">{{ short_url }}</a>
            </div>
        </body>
        </html>
    """, short_url=short_url)

# Redirect shortened URL to original URL
@app.route('/<string:shortcode>')
def redirect_to_original_url(shortcode):
    original_url = get_original_url(shortcode)
    if original_url:
        return redirect(original_url)
    else:
        return "URL not found"

# Initialize database
def init_db():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY, original_url TEXT, shortcode TEXT)''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
