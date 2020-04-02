from .db import db
import datetime
import pytz as pytz
from Main.settings.config import local_timezone


def local_timezone_conversion(utc_datetime):
    local_dt = utc_datetime.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_timezone.normalize(local_dt)


class User(db.Document):
    company_name = db.StringField(required=True, unique=True)
    phone_number = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    address = db.StringField(null=True)
    last_login = db.DateTimeField()
    created_date = db.DateTimeField(default=local_timezone_conversion(datetime.datetime.now()))
    is_active = db.BooleanField(default=False)
    is_admin = db.BooleanField(default=False)

    def __str__(self):
        return "Name - {}".format(self.company_name)


class UserOTP(db.Document):
    user = db.ReferenceField(User)
    otp = db.IntField()
    otp_time = db.DateTimeField(default=local_timezone_conversion(datetime.datetime.now()))
    otp_counter = db.IntField()
    is_verified = db.BooleanField(default=False)
    password_reset_uuid = db.StringField(required=False)


class Token(db.Document):
    key = db.StringField(required=True)
    created = db.DateTimeField(default=local_timezone_conversion(datetime.datetime.now()), required=True)
    user = db.ReferenceField(User)

    def __str__(self):
        return "Key - {}".format(self.key)

# import datetime
# print(datetime.datetime.now())
