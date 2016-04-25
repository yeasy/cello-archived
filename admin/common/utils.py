CLUSTER_API_PORT_START = 5000

CODE_OK=200
CODE_FAIL=400
CODE_NOT_FOUND=404

status_response_ok = {
    "code": CODE_OK,
    "error": None,
    "data": {}
}

status_response_fail = {
    "code": CODE_FAIL,
    "error": None,
    "data": {}
}
