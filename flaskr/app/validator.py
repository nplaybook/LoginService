from marshmallow import Schema, fields

class UserRegister(Schema):
    email = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)

class UserLogin(Schema):
    email = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)