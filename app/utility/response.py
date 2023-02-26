class Response:
    def success(data):
        response = {
            'success': True,
            'data': data
        }
        return response

    def failure(message, data=None):
        response = {
            'success': False,
            'error': message
        }
        if data is not None:
            response['data'] = data
        return response
