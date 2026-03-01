from flask import Flask, render_template, request, redirect
import requests
app = Flask(__name__)
API_URL = "http://localhost:500/v1/usuarios/"


@app.route("/")
def hello():
    return "¡Hola, Flask!"

if __name__ == "__main__":
    app.run(port=5010)
