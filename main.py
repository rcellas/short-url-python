from flask import Flask, render_template, redirect, request, abort, url_for
import string
import random
import logging

app = Flask(__name__)
shortened_urls = {}

# Configurar el registro de logs
logging.basicConfig(level=logging.INFO)

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()
        shortened_urls[short_url] = long_url
        app.logger.info(f"URL acortada creada: {short_url} -> {long_url}")
        short_url = f"{request.url_root}{short_url}"
    
    return render_template('index.html', short_url=short_url)

@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        app.logger.info(f"Redirigiendo {short_url} a {long_url}")
        return redirect(long_url)
    else:
        app.logger.warning(f"URL no encontrada: {short_url}")
        abort(404, description="URL not found")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)