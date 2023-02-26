from marshmallow.exceptions import ValidationError

from app.utility import Response

class AppException(Exception):
    def __init__(self, message, status_code=None, root_ex=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.root_ex = root_ex

    def __repr__(self):
        return f'{self.__class__.__name__}(message={self.message}, status_code={self.status_code}, root_ex={self.root_ex})'

def setup_error_handler(app):
    @app.errorhandler(ValidationError)
    def handle_validation_exception(ex):
        return Response.failure(ex.messages), 400

    @app.errorhandler(AppException)
    def handle_exception(ex):
        app.logger.error('Exception: %s', ex.message)
        app.logger.exception('Root Exception: %s', ex.root_ex)
        return Response.failure(ex.message), ex.status_code or 500

    @app.errorhandler(Exception)
    def handle_fatal_or_unexpected_exception(ex):
        app.logger.exception('Fatal Exception: %s', ex)
        return Response.failure('Internal Server Error'), 500
