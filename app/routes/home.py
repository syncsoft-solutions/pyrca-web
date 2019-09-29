from app.routes import app
from flask import jsonify


@app.route('/')
def main():
    return jsonify({'message': 'Welcome to pyrca-web!'})
