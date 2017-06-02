import datetime
from . import models

server_URL = 'http://192.168.0.9' # 바뀌지 않는 서버 주소 상수 값을 저장하세요
#server_URL = 'google.com' # 바뀌지 않는 서버 주소 상수 값을 저장하세요


def statusSend(txt):
    # txt는 .(온점) 으로 구분되며 다음과 같은 형식으로 들어옵니다. 아두이노id.온도값.습도값.수위값.조도값
    # mreq = requests.get(arduino.server_URL+'/status')
    result = [x for x in txt.split('.')]
    if len(result) >= 5:
        arduino_id = str(result[0])
        temperature = int(result[1])
        humidity = int(result[2])
        water_level = int(result[3])
        sun_light = int(result[4])
    else: return "invalid request information"

    newStatus = models.plant_status(arduino_id, humidity, temperature, 0, 0)  # 마지막 0 두개는 수위랑 조도
    models.db.session.add(newStatus)  # 여기서 에러 발생
    models.db.session.commit()

    cur_ardu = models.arduino.query.filter_by(arduino_id=arduino_id).first()
    if (cur_ardu == None): # 새 아두이노 등록
        newArduino = models.arduino(arduino_id)
        models.db.session.add(newArduino)
        models.db.session.commit()
        cur_ardu = models.arduino.query.filter_by(arduino_id=arduino_id).first()
        return "arduino registered. ID: "+arduino_id
    elif (cur_ardu.water_flag == True):
        cur_ardu.water_flag = False
        models.db.session.commit()
        return "1"  # 아두이노가 1을 받으면 물을 줍니다.
    elif (cur_ardu.led_on_flag == True):
        cur_ardu.led_on_flag = False
        models.db.session.commit()
        return "2"  # 2를 받으면 조명을 킵니다.
    elif (cur_ardu.led_off_flag == True):
        cur_ardu.led_off_flag = False
        models.db.session.commit()
        return "3"  # 3을 받으면 조명을 끕니다.
    elif (cur_ardu.flush_flag == True):
        cur_ardu.flush_flag = False
        models.db.session.commit()
        return "flush"

    return "status_recorded, humidity: " + str(humidity)


def ledOn(arduino_id):
    cur_ardu = models.arduino.query.filter_by(arduino_id=arduino_id).first()
    if(cur_ardu != None):
        cur_ardu.led_on_flag = True
        models.db.session.commit()
        return "led flag set to on ID: "+str(arduino_id)
    else: return "no arduino found with ID:"+str(arduino_id)

def ledOff(arduino_id):
    cur_ardu = models.arduino.query.filter_by(arduino_id=arduino_id).first()
    if(cur_ardu != None):
        cur_ardu.led_off_flag = True
        models.db.session.commit()
        return "led flag set to off ID: "+str(arduino_id)
    else: return "no arduino found with ID:"+str(arduino_id)

def flush(arduino_id):
    cur_ardu = models.arduino.query.filter_by(arduino_id=arduino_id).first()
    if(cur_ardu != None):
        cur_ardu.flush_flag =True
        models.db.session.commit()
        return "led flag set to off ID: " + str(arduino_id)
    else:
        return "no arduino found with ID:" + str(arduino_id)







#
#
#
# class ArduinoDelayManager:
#     delay = 2000 #기본 딜레이는 2초
#     last_time_stamp = datetime.datetime.utcnow()
#
#     def check_delay(self):
#         return self.delay
#
#     def set_current_time(self):
#         self.last_time_stamp = datetime.datetime.utcnow()
#
#     def check_last_stamp(self, last_time_stamp):
#         if last_time_stamp + 60000 < datetime.datetime.utcnow():  # 마지막 접속 후 1분이 지났다면
#             self.delay = 60000  # 아두이노 딜레이를 1분으로 바꿉니다.
#             return self.delay
#
