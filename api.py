
from flask_restful import Resource, reqparse
from urllib import parse
from flask import request, jsonify
from flask_restful_swagger_2 import swagger, Schema
from config import Config
import sys

parser = reqparse.RequestParser()
parser.add_argument('source', type=str, required=True, location=['form'], help='Source can not blank')
parser.add_argument('target', type=str, required=True, location=['form'], help='Target can not blank')
parser.add_argument('amount', type=float, required=True, location=['form'], help='Amount can not blank')


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


class TextModel(Schema):
    type = 'object'
    properties = {
        'source': {
            'type': 'string'
        },
        'target': {
            'type': 'string'
        },
        'amount': {
            'type': 'float'
        }
    }
    required = ['source','target','amount']


class CurrenciesChangeResource(Resource):
    @swagger.doc({
        'tags': ['Currencies Change'],
        'description': 'Change money from source to target',
        'parameters': [
            {
                'name': 'source',
                'description': '來源幣別',
                'in': 'formData',
                'type': 'string',
                'required': 'true'
            },
            {
                'name': 'target',
                'description': '目標幣別',
                'in': 'formData',
                'type': 'string',
                'required': 'true'
            },
            {
                'name': 'amount',
                'description': '金額數字',
                'in': 'formData',
                'type': 'number',
                'required': 'true'
            }
        ],
        'responses': {
            '0': {
                'description': 'Success',
                'schema': TextModel,
                'examples': {
                    'application/json': {
                        'code': 0,
                        'result': {
                            'amount': 'string'
                        }
                    }
                }
            },
            '4X': {
                'description': 'Import data Error',
                'schema': TextModel,
                'examples': {
                    'application/json': {
                        'code': '4X',
                        'result': {
                            'error': 'message'
                        }
                    }
                }
            },
            '50': {
                'description': 'Output amount over the Max',
                'schema': TextModel,
                'examples': {
                    'application/json': {
                        'code': 50,
                        'result': {
                            'error': 'message'
                        }
                    }
                }
            },
            '60': {
                'description': 'Other Error',
                'schema': TextModel,
                'examples': {
                    'application/json': {
                        'code': 60,
                        'result': {
                            'error': 'message'
                        }
                    }
                }
            }
        }
    })
    def post(self):
        args = parser.copy().remove_argument('file').parse_args()
        source = args['source']
        target = args['target']
        amount = args['amount']
        check_list = Config.CHECK_LIST
        if source not in check_list or target not in check_list:
            return jsonify({'code': 40,'result': {'error': 'Source or Target is invalidate'}})
        if amount < 0 or amount >= sys.float_info.max:
            return jsonify({'code': 41,'result': {'error': 'amount should >= 0 or < {}'.format(sys.float_info.max)}})
        try:
            if source == 'TWD':
                if target == 'JPY':
                    ans = half_up(amount * Config.TWD_TO_JPY)
                    return response_result(ans)
                elif target == 'TWD':
                    ans = half_up(amount)
                    return response_result(ans)
                else:
                    ans = half_up(amount * Config.TWD_TO_USD)
                    return response_result(ans)
            elif source == 'JPY':
                if target == 'JPY':
                    ans = half_up(amount)
                    return response_result(ans)
                elif target == 'TWD':
                    ans = half_up(amount * Config.JPY_TO_TWD)
                    return response_result(ans)
                else:
                    ans = half_up(amount * Config.JPY_TO_USD)
                    return response_result(ans)
            else:
                if target == 'JPY':
                    ans = half_up(amount * Config.USD_TO_JPY)
                    return response_result(ans)
                elif target == 'TWD':
                    ans = half_up(amount * Config.USD_TO_TWD)
                    return response_result(ans)
                else:
                    ans = half_up(amount)
                    return response_result(ans)
        except Exception as e:
            return jsonify({'code': 60,'result': {'error': e}})







