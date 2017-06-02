from app import application
from app import socketio




if __name__ == '__main__':
   socketio.run(application, debug=True, host='0.0.0.0')

