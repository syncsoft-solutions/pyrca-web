from app import app, api
from flask import jsonify, request

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

    # Do some checking for nodes for the main section.
    if not _main_section_args:
        return jsonify(has_error('Main section nodes not defined.'))

    if len(_main_section_args) < 3:
        return jsonify(has_error('Main section nodes must be equal or more than 3.'))

    _main_section = []
    for _ms in args['main_section']:
        _node: Node = Node(_ms[0], _ms[1])
        _main_section.append(_node)

    _section = Section()
    _section.set_main_section(_main_section)

    _bs = BeamSection()
    _bs.section = _section

    # Get the unit
    if 'unit' in args:
        if args['unit'] == 0:
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

    _bs.set_fc_prime(args['fc_prime'])                  # Set the f'c
    _bs.set_fy(args['fy'])                              # Set the fy
    _bs.set_effective_depth(args['effective_depth'])    # Set effective depth

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


def has_error(error_message):
    """
    Returns an error object.
    :param error_message:
    :return:
    """
    return {'has_error': True, 'error_message': error_message}
