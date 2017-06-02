import datetime
from . import models
from flask import request

server_URL = 'http://192.168.0.9' # 바뀌지 않는 서버 주소 상수 값을 저장하세요
#server_URL = 'google.com' # 바뀌지 않는 서버 주소 상수 값을 저장하세요

def status_send(txt):
    result = [x for x in txt.split('.')]
    if len(result) >= 5:
        arduino_id = str(result[0])
        temperature = int(result[1])
        humidity = int(result[2])
        water_level = int(result[3])
        sun_light = int(result[4])
    else: print( "invalid request information")

    newStatus = models.plant_status(arduino_id, humidity, temperature, 0, 0)  # 마지막 0 두개는 수위랑 조도
    models.db.session.add(newStatus)  # 여기서 에러 발생
    models.db.session.commit()

    cur_ardu = models.arduino.query.filter_by(arduino_id=arduino_id).first()
    if (cur_ardu == None): # 새 아두이노 등록
        print( "There is no arduino with ID: "+arduino_id)

    print( "status_recorded, humidity: " + str(humidity))


def arduino_in(message):
    arduino_id = str(message['id'])
    print("arduino id: "+arduino_id)
    sid = request.sid
    cur_ardu = models.arduino.query.filter_by(arduino_id=arduino_id).first()

    if (cur_ardu == None): # 새 아두이노 등록
        newArduino = models.arduino(arduino_id)
        models.db.session.add(newArduino)
        models.db.session.commit()
        cur_ardu = models.arduino.query.filter_by(arduino_id=arduino_id).first()
        print( "New arduino registered. ID: "+arduino_id)

    cur_ardu.sid = str(request.sid)
    models.db.session.commit()
    print("arduino "+arduino_id+" Loged in: "+sid)
    #emit("this is emit message from def  echo_message")