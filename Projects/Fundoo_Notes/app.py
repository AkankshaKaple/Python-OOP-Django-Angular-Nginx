import datetime
from errors import KeyNotFound, DataNotFound, InvalidCredentials
from bson import ObjectId
from pymongo import MongoClient
from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from config import Config
from helper import get_custom_response, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

app = Flask(__name__)

cors = CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = Config.SECRET_KEY

api = Api(app)  # This will be use for Swagger

database = Config.Mongodb.database_name[0]
username = Config.Mongodb.username[0]
password = Config.Mongodb.password
port = 27017
server_address = Config.Mongodb.host[0]

uri = "mongodb://{}:{}@{}:{}/{}".format(username, password, server_address, port, database)

client = MongoClient(uri)
db = client.fundooNote

parser = api.parser()
parser.add_argument('token', location='headers')

create_note_api = api.model('CreateNote',
                            {
                                "title": fields.String(),
                                "description": fields.String()
                            })

delete_note = api.model('delete_note',
                        {
                            'note_id': fields.String()
                        })

edit_note = api.model('edit_note',
                      {
                          "title": fields.String(),
                          "description": fields.String()

                      })


@api.route('/note')
class Note(Resource):

    @api.doc(params={"user_id": "Enter user Id"})
    def get(self):
        user_id = request.args['user_id']
        all_notes = list(db.Note.find({'user_id': str(user_id)}).sort("datetime", -1))
        note_list = []
        for note in all_notes:
            note_list.append({
                '_id': str(note['_id']),
                'title': note['title'],
                'description': note['description']
            })
        return get_custom_response(success=True, message="List of all the notes for this user", data=note_list,
                                   status_code=201)

    @api.expect(create_note_api)
    def post(self):
        try:
            requested_data = request.get_json()
            user_id = request.args['user_id']
            print(requested_data)
        except:
            return get_custom_response(message="It seems you have a syntax error, please take a look.")

        print("len : ", len(requested_data['title'].strip()))
        print("description : ", len(requested_data['description'].strip()))
        if len(requested_data['title'].strip()) == 0 and (len(requested_data['description']) == 0):
            return get_custom_response(message="Enter title or description.")

        else:
            print("Continue")

        dt_utcnow = datetime.datetime.now(tz=pytz.UTC)
        dt_mnt = dt_utcnow.astimezone(pytz.timezone('Asia/Kolkata'))

        requested_data['datetime'] = dt_mnt
        requested_data['user_id'] = user_id

        print("Req : ", requested_data)
        db.Note.insert(requested_data)
        print("Note is created")
        return get_custom_response(success=True,
                                   message="Note is created",
                                   status_code=201)

    @api.expect(delete_note)
    def delete(self):
        try:
            requested_data = request.get_json()
            print("note_id : ", requested_data['note_id'])
        except:
            return get_custom_response(message="It seems you have a syntax error, please take a look.")

        db.Note.delete_one({'_id': ObjectId(requested_data['note_id'])})
        return get_custom_response(success=True, message="Note is deleted successfully", status_code=201)

    @api.expect(edit_note)
    @api.doc(params={"note_id": "Enter node Id"})
    def patch(self):
        try:
            requested_data = request.get_json()
            note_id = request.args['note_id']
            print("requested_data : ", requested_data)
        except:
            return get_custom_response(message="It seems you have a syntax error, please take a look.")

        if len(requested_data['title'].strip()) == 0 and len(requested_data['description']) == 0:
            return get_custom_response(message="Enter title or description.")

        document_obj = db.Note.find_one({'_id': ObjectId(note_id)})
        print("document_obj : ", list(db.Note.find_one({'_id': ObjectId(note_id)})))

        dt_utcnow = datetime.datetime.now(tz=pytz.UTC)
        dt_mnt = dt_utcnow.astimezone(pytz.timezone('Asia/Kolkata'))

        print("requested_data : ", requested_data)
        db.Note.update_one({'_id': ObjectId(note_id)}, {"$set": {
            'title': requested_data['title'],
            'description': requested_data['description'],
            'datetime': dt_mnt
        }})

        return get_custom_response(success=True, message="Note updated successfully.", status_code=201)


registration_model = api.model('Registration Model',
                               {'email_id': fields.String(required=True, description='Enter Your Email Id'),
                                'password': fields.String(required=True, description='Enter Your Password')
                                })


@api.route('/register')
class UserInformation(Resource):

    @api.expect(registration_model)
    def post(self):
        try:
            requested_data = request.get_json()
            print("requested_data : ", requested_data)
            user_email_id = requested_data.get('email_id', None)
            user_password = requested_data.get('password', None)


            if user_email_id is None or user_password is None:
                raise KeyNotFound

            elif len(user_email_id) == 0 or len(user_password) == 0:
                raise DataNotFound

            hashed_password = generate_password_hash(user_password)
            db.Registration.insert_one({'email_id': user_email_id,
                                        'password': hashed_password})

            response = get_custom_response(success=True, message="Registration Successful.", status_code=201)

        except DataNotFound:
            response = get_custom_response(message="Email id or password cannot be empty.")

        except KeyNotFound:
            response = get_custom_response(message="Email id or password is empty.")

        except ConnectionError:

            response = get_custom_response(message="You might have connection issue.",
                                           status_code=503)
        return response


login_model = api.model('Login Model', {'email_id': fields.String(required=True, description='Enter Your Email Id'),
                                        'password': fields.String(required=True,
                                                                  description='Enter Your Password')
                                        })


@api.route('/login')
class LoginModel(Resource):

    @api.expect(login_model)
    def post(self):
        try:
            requested_data = request.get_json()
            email_id = requested_data.get('email_id', None)
            password = requested_data.get('password', None)
            print("requested_data : ", requested_data)

            if email_id is None or password is None:
                raise KeyNotFound

            elif len(email_id) == 0 or len(password) == 0:
                raise DataNotFound
            user_doc_obj = db.Registration.find_one({'email_id': email_id})

            if user_doc_obj is None:
                print("user_doc_obj : ", user_doc_obj)
                raise InvalidCredentials

            stored_password = user_doc_obj['password']
            is_authenticate = check_password_hash(stored_password, password)

            if is_authenticate:

                key = 'Key'
                payload = {
                    'email_id': email_id
                }
                algorithm = 'HS256'
                encoded_token = jwt.encode(payload=payload, key=key, algorithm=algorithm).decode('utf-8')

                response = get_custom_response(success=True, message='You Logged In Successfully', token=encoded_token,
                                               status_code=200)

            else:
                response = get_custom_response(success=False, message='Invalid Credentials')

        except InvalidCredentials:
            response = get_custom_response(message="Email address is not registered.")

        except DataNotFound:
            response = get_custom_response(message="Email id or password cannot be empty.")

        except KeyNotFound:
            response = get_custom_response(message="Email id or password is empty.")

        except ConnectionError:

            response = get_custom_response(message="You might have connection issue.",
                                           status_code=503)
        return response


@api.route('/logout')
class Logout(Resource):
    @api.expect(parser)
    @login_required
    def get(self):  # Logout method

        """
        This Api is used to logout user

        :return: status
        """

        response = get_custom_response(success=True,
                                       message='You are Logged out successfully'
                                       , status_code=200
                                       )
        return response


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=True, threaded=True)
