class Response:
    def success(data, extra_dict=None):
        response = {
            'success': True,
            'data': data
        }
        if (extra_dict is not None):
            for k, v in extra_dict.items():
                response[k] = v
        return response

    def failure(message, data=None):
        response = {
            'success': False,
            'error': message
        }
        if data is not None:
            response['data'] = data
        return response
