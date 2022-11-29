
from apps.flask.model import db


class PhoneBindInfo(db.Model):
    __tablename__ = "phone_bind_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    token = db.Column(db.String(200), default="")
    match_car_type = db.Column(db.String(500), default="")
    screen_car_type = db.Column(db.String(500), default="")
    target_address = db.Column(db.String(500), default="")
    screen_address = db.Column(db.String(500), default="")
    min_price = db.Column(db.Integer, default=0)
    min_distance = db.Column(db.Integer, default=0)
    max_distance = db.Column(db.Integer, default=1000)
    creat_time = db.Column(db.DateTime, nullable=True)
    update_time = db.Column(db.DateTime, nullable=True)
    is_status = db.Column(db.Boolean, default=True)