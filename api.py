# -*- coding: utf-8 -*-

from flask import Flask, Response, Request
import json

app = Flask(__name__)


@app.route('/api/profile', methods=['POST', 'GET'])
def get_profile():
    resp = Response(json.dumps('{"status" : "PONG"}'))
    resp.headers.add("Content-Type", "application/json")
    resp.headers.add("Access-Control-Allow-Origin", "*")
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=7000)