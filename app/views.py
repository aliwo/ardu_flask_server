from app import application, socketio, emit, join_room, leave_room, \
    close_room, rooms, disconnect, send
from flask import request, jsonify, request
#import requests, re
from . import models, moblie, arduino

@application.route('/')
def hello_world():
    models.db.create_all()  # db를 만듭니다.
    return 'DB created\n'

#아두이노가 들어오는 경로
@socketio.on('arduino_in')
def arduino_in(message):
    return arduino.arduino_in(message)

@socketio.on('status_send')
def status_send(message):
    status = message['status']
    return arduino.status_send(status)

@socketio.on('connect')
def connected_message():
    pass

@application.route('/status_send/<string:txt>', methods=['GET']) #/<string:txt>', methods=['GET']
def status_send(txt):
    if request.method == 'GET':
        return arduino.statusSend(txt)



#안드로이드가 들어오는 경로
@application.route('/water/<string:id>', methods=['GET'])
def water(id):
    return moblie.water(id)

@application.route('/status_get', methods=['GET'])
def status_get():
    status = models.plant_status.query.order_by(models.plant_status.created_at.desc()).first() # desc 를 넣으면 가장 최근 레코드가 뜸 ^^
    result = {"temperature":status.temperature, "humidity":status.humidity, "water_level":status.water_level }
    return jsonify(result)

@application.route('/led_on/<string:id>', methods=['GET'])
def led_on(id):
    return moblie.led_on(id)

@application.route('/led_off/<string:id>', methods=['GET'])
def led_off(id):
    return moblie.led_off(id)

@application.route('/flush/<string:id>', methods=['GET'])
def flush_arduino(id):
    return moblie.flush(id)
