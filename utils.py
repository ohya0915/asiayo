import sys
from flask import jsonify


def half_up(data):
    n = data * 1000 % 10
    try:
        if n >= 5:
            return format((int(data * 100) + 1) / 100, ',')
        else:
            return format(int(data * 100) / 100, ',')
    except:
        return jsonify({'code': 50,'result': {'error': 'amount is over {}!'.format(sys.float_info.max)}})


def response_result(data):
    if not isinstance(data, str):
        return data
    return jsonify({'code': 0,'result': {'amount': data}})

