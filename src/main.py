#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sqlite3
import datetime
from flask import Flask, jsonify, make_response, render_template, request
from start import create_app
from db import Database
from user import User

app = Flask(__name__)
app = create_app()
filename = os.getenv("DB", "/app/users.db")
db = Database(app, filename)

@app.route('/status', methods=['GET'])
def get_status():
    app.logger.info("get_status")
    """
    Get the status of the api server
    """
    return make_response(jsonify({'status': 'Up and running'}), 200)

@app.route('/hola/')
@app.route('/hola/<nombre>')
def saluda(nombre=None):
    app.logger.info("saluda")
    return render_template("hola.html",nombre=nombre)

@app.route('/input')
def input():
    app.logger.info("input")
    return render_template("input.html")

@app.route('/list')
def list():
    app.logger.info("list")
    sql = "SELECT * FROM users"
    items = db.select(sql)
    users = []
    for item in items:
        users.append(User(item))
    app.logger.info(users)
    return render_template("list.html", users=users)

@app.route('/data', methods=['POST'])
def data():
    app.logger.info("data")
    app.logger.debug(request.form)
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    sql = "INSERT INTO users (fname, lname) VALUES (? , ?)"
    db.execute(sql, (fname, lname))
    return render_template("hola.html",nombre=fname)

@app.errorhandler(404)
def not_found(error):
    app.logger.error(error)
    """
    When not found

    :param error str: A json with the error
    """
    return render_template("404.html")
