from flask import Flask
from app.extensions import socketio
from app.main import blueprint as main_blueprint
from app.user import blueprint as user_blueprint
from app.bucket import blueprint as bucket_blueprint
from app.admin import blueprint as admin_blueprint
from app.chatting import blueprint as chatting_blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = 'bsdajvkbakjbfoehihewrpqkldn21pnifninelfbBBOIQRqnflsdnljneoBBOBi2rp1rp12r9uh'

    # 블루프린트 등록
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(bucket_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(chatting_blueprint)

    # SocketIO 초기화
    socketio.init_app(app)

    return app