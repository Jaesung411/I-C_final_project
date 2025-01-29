from flask import * 
from flask_socketio import *
from app import socketio

blueprint = Blueprint('chatting', __name__, url_prefix='/chatting' ,template_folder='templates')

# 클라이언트 ID별 채팅방 데이터 저장
clients = {
    "client1": [],
    "client2": []
}

# 소켓 이벤트 핸들러: 특정 채팅방 참여
@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f"{session['login_info']['username']} 님이 {room}에 참여했습니다."}, room=room)

# 소켓 이벤트 핸들러: 메시지 전송
@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    # 메시지 저장
    clients[room].append({'user': session['login_info']['username'], 'message': message})
    # boardcast 
    emit('message', {'user': session['login_info']['username'], 'message': message}, room=room)

# 소켓 이벤트 핸들러: 특정 채팅방 나가기
@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f"{session['login_info']['username']} 님이 {room}에서 나갔습니다."}, room=room)
