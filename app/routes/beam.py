from app import app, api
from flask import jsonify, request

from pyrca.properties.node import Node
from pyrca.properties.section import Section
from pyrca.properties.beam_section import BeamSection


@app.route('/beam-balanced-analysis', methods=['POST'])
def beam_balanced_analysis():
    args = request.json

    _main_section = []

    if args['main_section']:
        for _ms in args['main_section']:
            _node: Node = Node(_ms[0], _ms[1])
            _main_section.append(_node)

    print(_main_section)

    return jsonify({})


def has_error(error_message):
    """
    Returns an error object.
    :param error_message:
    :return:
    """
    return {'has_error': True, 'error_message': error_message}
