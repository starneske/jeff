from flask_restful_swagger_2 import Schema

from qube.src.api.swagger_models.jeff import jeffErrorModel
from qube.src.api.swagger_models.jeff import jeffModel
from qube.src.api.swagger_models.jeff import jeffModelPostResponse

"""
the common response messages printed in swagger UI
"""

post_response_msgs = {
    '201': {
        'description': 'CREATED',
        'schema': jeffModelPostResponse
    },
    '401': {
        'description': 'Unauthorized'
    },
    '400': {
        'description': 'Bad Request'
    },
    '404': {
        'description': 'Not found'
    },
    '500': {
        'description': 'Internal server error',
        'schema': jeffErrorModel
    }
}

get_response_msgs = {
    '200': {
        'description': 'OK',
        'schema': jeffModel
    },
    '401': {
        'description': 'Unauthorized'
    },
    '400': {
        'description': 'Bad Request'
    },
    '404': {
        'description': 'Not found'
    },
    '500': {
        'description': 'Internal server error',
        'schema': jeffErrorModel
    }
}

put_response_msgs = {
    '204': {
        'description': 'No Content'
    },
    '401': {
        'description': 'Unauthorized'
    },
    '400': {
        'description': 'Bad Request'
    },
    '404': {
        'description': 'Not found'
    },
    '500': {
        'description': 'Internal server error',
        'schema': jeffErrorModel
    }
}

del_response_msgs = {
    '204': {
        'description': 'No Content'
    },
    '401': {
        'description': 'Unauthorized'
    },
    '400': {
        'description': 'Bad Request'
    },
    '404': {
        'description': 'Not found'
    },
    '500': {
        'description': 'Internal server error',
        'schema': jeffErrorModel
    }
}

response_msgs = {
    '200': {
        'description': 'OK'
    },
    '401': {
        'description': 'Unauthorized'
    },
    '400': {
        'description': 'Bad Request'
    },
    '404': {
        'description': 'Not found'
    },
    '500': {
        'description': 'Internal server error'
    }
}


class ErrorModel(Schema):
    type = 'object'
    properties = {
        'error_code': {
            'type': 'string'
        },
        'error_message': {
            'type': 'string'
        }
    }
