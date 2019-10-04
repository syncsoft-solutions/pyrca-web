from app import app, api
from flask import jsonify, request
import ast

from pyrca.properties.node import Node
from pyrca.properties.section import Section
from pyrca.properties.beam_section import BeamSection
from pyrca.properties.steel_tension import SteelTension
from pyrca.properties.steel_compression import SteelCompression
from pyrca.properties.unit import Unit
from pyrca.analysis.beam_analyses import BeamAnalyses
from pyrca.analysis.beam_analysis_result import BeamAnalysisResult
from pyrca.analysis.stress_distribution import StressDistribution


@app.route('/beam-balanced-analysis', methods=['POST'])
def beam_balanced_analysis():
    _sd = StressDistribution.WHITNEY
    args = request.json

    _main_section_args = args['main_section']
    _main_section_args = ast.literal_eval(_main_section_args)

    # Do some checking for nodes for the main section.
    if not _main_section_args:
        return jsonify(has_error('Main section nodes not defined.'))

    if len(_main_section_args) < 3:
        return jsonify(has_error('Main section nodes must be equal or more than 3.'))

    _main_section = []
    for _ms in _main_section_args:
        _node: Node = Node(_ms[0], _ms[1])
        _main_section.append(_node)

    _clippings = []

    if 'clippings' in args:
        _clipping_args = args['clippings']
        _clipping_args = ast.literal_eval(_clipping_args)
        if args['clippings']:
            for _clipping_args in args['clippings']:
                _clipping = []
                for _clip_node in _clipping_args:
                    _clipping.append(Node(_clip_node[0], _clip_node[1]))
                _clippings.append(_clipping)

    _section = Section()
    _section.set_main_section(_main_section)
    _section.set_clippings(_clippings)

    _bs = BeamSection()
    _bs.section = _section

    # Get the unit
    if 'unit' in args:
        if int(args['unit']) == 0:
            _bs.unit = Unit.ENGLISH

    if 'fc_prime' not in args:
        return jsonify(has_error('F\'c not defined.'))

    if 'fy' not in args:
        return jsonify(has_error('Fy not defined.'))

    if 'effective_depth' not in args:
        return jsonify(has_error('Effective depth not defined.'))

    if 'stress_distribution' in args:
        # In the frontend, indicate 0 for parabolic and 1 for whitney
        if int(args['stress_distribution']) == 0:
            _sd = StressDistribution.PARABOLIC

    _bs.set_fc_prime(float(args['fc_prime']))                  # Set the f'c
    _bs.set_fy(float(args['fy']))                              # Set the fy
    _bs.set_effective_depth(float(args['effective_depth']))    # Set effective depth

    _steel_tension = SteelTension()
    _steel_compression = SteelCompression()

    _bs.steel_tension = SteelTension()
    _bs.steel_compression = _steel_compression

    _analyses = BeamAnalyses()
    _analyses.beam_section = _bs
    _result: BeamAnalysisResult = _analyses.beam_balanced_analysis(_sd)

    return jsonify({'tension_steel': _analyses.balanced_steel_tension,
                    'moment': _result.moment_c,
                    'curvature': _result.curvature_c,
                    'kd': _result.kd})


@app.route('/beam-capacity-analysis', methods=['POST'])
def beam_capacity_analysis():
    _sd = StressDistribution.WHITNEY
    args = request.get_json()

    if not args:
        return has_error('JSON request can\'t be parsed.')

    _main_section_args = args['main_section']
    _main_section_args = ast.literal_eval(_main_section_args)

    # Do some checking for nodes for the main section.
    if not _main_section_args:
        return jsonify(has_error('Main section nodes not defined.'))

    if len(_main_section_args) < 3:
        return jsonify(has_error('Main section nodes must be equal or more than 3.'))

    _main_section = []
    for _ms in _main_section_args:
        _node: Node = Node(_ms[0], _ms[1])
        _main_section.append(_node)

    _clippings = []

    if 'clippings' in args:
        _clipping_args = args['clippings']
        _clipping_args = ast.literal_eval(_clipping_args)
        if _clipping_args:
            for _clipping_args in args['clippings']:
                _clipping = []
                for _clip_node in _clipping_args:
                    _clipping.append(Node(_clip_node[0], _clip_node[1]))
                _clippings.append(_clipping)

    _section = Section()
    _section.set_main_section(_main_section)
    _section.set_clippings(_clippings)

    _bs = BeamSection()
    _bs.section = _section

    if 'unit' in args:
        if int(args['unit']) == 0:
            _bs.unit = Unit.ENGLISH

    if 'fc_prime' not in args:
        return jsonify(has_error('F\'c not defined.'))

    if 'fy' not in args:
        return jsonify(has_error('Fy not defined.'))

    if 'effective_depth' not in args:
        return jsonify(has_error('Effective depth not defined.'))

    if 'stress_distribution' in args:
        # In the frontend, indicate 0 for parabolic and 1 for whitney
        if args['stress_distribution'] == 0:
            _sd = StressDistribution.PARABOLIC

    if 'As' not in args:
        return jsonify(has_error('Tensile reinforcement area (As) not defined.'))

    _bs.set_fc_prime(float(args['fc_prime']))  # Set the f'c
    _bs.set_fy(float(args['fy']))  # Set the fy
    _bs.set_effective_depth(float(args['effective_depth']))  # Set effective depth

    _steel_tension = SteelTension()
    _steel_tension.set_total_area(float(args['As']), _bs.unit)

    _steel_compression = SteelCompression()
    if 'As_Prime' in args:
        _steel_compression.set_total_area(float(args['As_Prime']), _bs.unit)

    _bs.steel_tension = _steel_tension
    _bs.steel_compression = _steel_compression

    _analyses = BeamAnalyses()
    _analyses.beam_section = _bs
    _result = _analyses.beam_capacity_analysis(_sd)

    return jsonify({'moment': _result.moment_c,
                    'curvature': _result.curvature_c,
                    'kd': _result.kd})


def has_error(error_message):
    """
    Returns an error object.
    :param error_message:
    :return:
    """
    return {'has_error': True, 'error_message': error_message}
