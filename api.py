
from flask_restful import Resource, reqparse
from flask import jsonify
from flask_restful_swagger_2 import swagger, Schema
from config import Config
from utils import half_up, response_result
import sys

parser = reqparse.RequestParser()
parser.add_argument('source', type=str, required=True, location=['form'], help='Source can not blank')
parser.add_argument('target', type=str, required=True, location=['form'], help='Target can not blank')
parser.add_argument('amount', type=float, required=True, location=['form'], help='Amount can not blank')


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
        args = parser.copy().parse_args()
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
                    return response_result(half_up(amount * Config.TWD_TO_JPY))
                elif target == 'TWD':
                    return response_result(half_up(amount))
                else:
                    return response_result(half_up(amount * Config.TWD_TO_USD))
            elif source == 'JPY':
                if target == 'JPY':
                    return response_result(half_up(amount))
                elif target == 'TWD':
                    return response_result(half_up(amount * Config.JPY_TO_TWD))
                else:
                    return response_result(half_up(amount * Config.JPY_TO_USD))
            else:
                if target == 'JPY':
                    return response_result(half_up(amount * Config.USD_TO_JPY))
                elif target == 'TWD':
                    return response_result(half_up(amount * Config.USD_TO_TWD))
                else:
                    return response_result(half_up(amount))
        except Exception as e:
            return jsonify({'code': 60,'result': {'error': e}})







