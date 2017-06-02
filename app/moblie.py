from . import models
from app import socketio

#물 주기, led 켜기 끄기는 기능이 비슷하니까 한 번 합쳐 볼까?


#물을 주는 함수
def water(id):
    cur_ardu = models.arduino.query.filter_by(arduino_id=id).first()
    sid = cur_ardu.sid
    socketio.send({"data":"water"}, room=sid) # data 키의 값에 원하는 문자열을 집어 넣으면 아두이노가 그대로 parse 한다.
    return "message sent to sid:"+sid

#led를 켜는 함수
def led_on(id):
    cur_ardu = models.arduino.query.filter_by(arduino_id=id).first()
    sid = cur_ardu.sid
    socketio.send({"data":"led_on"}, room=sid) # data 키의 값에 원하는 문자열을 집어 넣으면 아두이노가 그대로 parse 한다.
    return "message sent to sid:"+sid

#led를 끄는 함수
def led_off(id):
    cur_ardu = models.arduino.query.filter_by(arduino_id=id).first()
    sid = cur_ardu.sid
    socketio.send({"data":"led_off"}, room=sid) # data 키의 값에 원하는 문자열을 집어 넣으면 아두이노가 그대로 parse 한다.
    return "message sent to sid:"+sid

def flush(id):
    pass