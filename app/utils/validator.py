from marshmallow import Schema, fields

class UserRegister(Schema):
    email = fields.Email(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)

class UserLogin(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserResetPassword(Schema):
    email = fields.Email(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)