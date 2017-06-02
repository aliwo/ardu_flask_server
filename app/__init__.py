from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect, send
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = 'secreet!'
application.config.from_object('config') # config 파일을 불러와서 app객체를 설정합니다.
async_mode =None
thread = None

db=SQLAlchemy(application)

socketio = SocketIO(application, async_mode= async_mode)

from app import views, models, arduino # import 자체가 아무 일도 하지 않는 것이 아님. views에 작성된 코드를 실행 하는 것 같다.

'''순환 참조(circular reference)를 막기 위해서 import views를 마지막에 한다.
app 객체를 먼저 만든 다음에 views를 부르면, views에서는 완성된 app 을 가져온다.
만약 import를 코드 맨 위에서 해 버리면 만들어지지도 않은 app 을 view가 가져오게 된다.
코드가 꼬여버리는 거임.
'''