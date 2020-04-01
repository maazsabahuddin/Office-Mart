from .db import db
import datetime
import pytz as pytz
from Main.settings.config import local_timezone


def local_timezone_conversion(utc_datetime):
    local_dt = utc_datetime.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_timezone.normalize(local_dt)


class User(db.Document):
    company_name = db.StringField(required=True, unique=True)
    phone_number = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    last_login = db.DateTimeField(default=local_timezone_conversion(datetime.datetime.now()))
    created_date = db.DateTimeField(default=local_timezone_conversion(datetime.datetime.now()))
    is_active = db.BooleanField(required=True, default=False)
    is_admin = db.BooleanField(default=False)


class UserOTP(db.Document):
    user = db.ReferenceField('User')
    otp = db.IntField()
    otp_time = db.DateTimeField(default=local_timezone_conversion(datetime.datetime.now()))
    otp_counter = db.IntField()
    is_verified = db.BooleanField(default=False)
    password_reset_uuid = db.StringField(required=False)


class Token(db.Document):
    key = db.StringField(required=True)
    created = db.DateTimeField(default=local_timezone_conversion(datetime.datetime.now()), required=True)
    user = db.ReferenceField('User')

# import datetime
# print(datetime.datetime.now())
