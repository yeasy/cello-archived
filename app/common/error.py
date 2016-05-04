CODE_OK = 200
CODE_CREATED = 201
CODE_NO_CONTENT = 204
CODE_BAD_REQUEST = 400
CODE_FORBIDDEN = 403
CODE_NOT_FOUND = 404
CODE_METHOD_NOT_ALLOWED = 405
CODE_NOT_ACCEPTABLE = 406
CODE_CONFLICT = 409

status_response_ok = {
    "status": "OK",
    "code": CODE_OK,
    "error": "",
    "data": "",
}

status_response_fail = {
    "status": "FAIL",
    "code": CODE_BAD_REQUEST,
    "data": "",
}


# not used, may deprecate later
errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': CODE_CONFLICT,
        'extra': "NA",
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': CODE_NOT_FOUND,
        'extra': "NA",
    },
    'InvalidParams': {
        'message': "Not valid param is given",
        'status': CODE_NOT_ACCEPTABLE,
        'extra': "NA",
    },
    'InvalidOperations': {
        'message': "Invalid operation method is given",
        'status': CODE_METHOD_NOT_ALLOWED,
        'extra': "NA",
    },
}
