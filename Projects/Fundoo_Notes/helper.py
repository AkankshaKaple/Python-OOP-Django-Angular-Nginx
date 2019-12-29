from flask import jsonify, request
import jwt

def get_custom_response(success=False,message="Something Went Wrong", data=[], token=None, status_code=400):
    if token is not None:
        response = {
            'success': success,
            'messgae': message,
            'token': token
        }
    else:
        response = {
            'success': success,
            'messgae': message,
            'data': data
        }
    return response


def login_required(method):
    def is_token_authenticated(reference_variable, *args, **kwargs):

        try:

            token=request.headers.get('token', None)
            if token is not None:

                return method(reference_variable, *args, **kwargs)

            else:

                response = get_custom_response(message='You Need To Login First')

        except jwt.ExpiredSignatureError :

            response = get_custom_response(message='Token is Expired')

        except Exception as e:
            response = get_custom_response(message=str(e))

        return response

    return is_token_authenticated
