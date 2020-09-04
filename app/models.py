from datetime import datetime
from app import db
from hashlib import md5


#АВС/ DEF;От;До;Емкость;Оператор;Регион
class PhoneRange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abcdef_code = db.Column(db.String(3))
    phone_start = db.Column(db.String(7))
    phone_end = db.Column(db.String(7))
    phones_total = db.Column(db.String(9))
    provider = db.Column(db.String(200))
    region = db.Column(db.String(200))
