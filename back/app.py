import json
import re

import requests
from flask import Flask, redirect, render_template, request, url_for
from .parser import Parser

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    parser = Parser()
    mail_url = 'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm'
    tracking_code = request.form["tracking"]
    data = {'acao': 'track', 'objetos': tracking_code, 'btnPesq': 'Buscar'}
    package_search = requests.post(mail_url, data=data)
    search_result = parser.parse(package_search.content, tracking_code)