from app import app
from flask import jsonify


@app.route('/beam/flexure/balance_analysis')
def balance_analysis():
    return jsonify({})