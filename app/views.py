from .arduino import *
from app import application
from flask import request, jsonify
import requests, re
from . import models

@application.route('/')
def hello_world():
    models.db.create_all()  # db를 만듭니다.
    return 'Hello Arduino\n'

@application.route('/status_send/<string:txt>', methods=['GET']) #/<string:txt>', methods=['GET']
def status_send(txt):
    if request.method == 'GET':
        return statusSend(txt)

@application.route('/status_get', methods=['GET'])
def status_get():
    status = models.plant_status.query.order_by(models.plant_status.created_at.desc()).first() # desc 를 넣으면 가장 최근 레코드가 뜸 ^^
    result = {"temperature":status.temperature, "humidity":status.humidity, "water_level":status.water_level }
    return jsonify(result)

@application.route('/water/<string:id>', methods=['GET'])
def water(id):
    cur_ardu = models.arduino.query.filter_by(arduino_id = id).first()
    if (cur_ardu != None):
        cur_ardu.water_flag = True
        models.db.session.commit()
        return "water flag set to on ID: " + str(id)
    else:
        return "no arduino found with ID:" + str(id)

@application.route('/led_on/<string:id>', methods=['GET'])
def led_on(id):
    return ledOn(id)

@application.route('/led_off/<string:id>', methods=['GET'])
def led_off(id):
    return ledOff(id)

@application.route('/flush/<string:id>', methods=['GET'])
def flush_arduino(id):
    return flush(id)

#
# @application.route('/check_delay/<string:txt>', methods=['GET'])
# def check_delay(txt):
#     arduino_id = txt
#     arduino_data = models.arduino.query.filter_by(arduino_id=arduino_id).first()
#
#     if arduino_data == None: # 만약 등록된 아두이노가 없으면
#         new_arduino = models.arduino(arduino_id)
#         models.db.session.add(new_arduino)
#         models.db.session.commit()
#         arduino_data = models.arduino.query.filter_by(arduino_id=arduino_id).first()
#
#     last_time_stamp = arduino_data.last_time_stamp
#     if last_time_stamp + 60000 < datetime.datetime.utcnow():  # 마지막 접속 후 1분이 지났다면
#         arduino_data.delay = 60000  # 아두이노 딜레이를 1분으로 바꿉니다.
#         models.db.session.commit()
#
#     #txt에 담긴 아두이노 아이디로 db를 조회해서 마지막 timestamp를 가져온다. 만약 없으면 db에 객체를 만든다.
#     return jsonify(arduino_data.delay)