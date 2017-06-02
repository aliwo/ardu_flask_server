import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db

class plant_status(db.Model):
    arduino_id = db.Column(db.String)
    created_at = db.Column(db.DateTime, primary_key=True, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    sun_light = db.Column(db.Integer, nullable=True) # 추후에 조도 센서 값 저장기능이 추가됩니다!
    water_level = db.Column(db.Integer, nullable=False)

    def __init__(self, arduino_id, humidity, temperature, water_level, sun_light):
        self.arduino_id = arduino_id
        self.created_at = datetime.datetime.utcnow()
        self.humidity = humidity
        self.temperature = temperature
        self.water_level = water_level
        self.sun_light = sun_light

class arduino(db.Model):
    arduino_id = db.Column(db.String, primary_key=True, unique=True)
    delay = db.Column(db.Integer)
    short_delay_time_stamp = db.Column(db.DateTime)
    water_flag = db.Column(db.BOOLEAN)
    led_on_flag = db.Column(db.BOOLEAN)
    led_off_flag = db.Column(db.BOOLEAN)
    flush_flag = db.Column(db.BOOLEAN)
    sid = db.Column(db.String)
    #plant_status = db.relationship()

    def __init__(self, id, delay=2000):
        self.arduino_id = id
        self.delay = delay
        self.short_delay_time_stamp = datetime.datetime.utcnow()
        self.water_flag = False
        self.led_on_flag = False
        self.led_off_flag = False
        self.flush_flag = False
        self.sid = "unknown"