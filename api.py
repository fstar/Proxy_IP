from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import VARCHAR, INTEGER, DATETIME,text
from flask_restful import Resource, Api
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from gevent.wsgi import WSGIServer
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
from flask_restful import reqparse


DB_URI = "mysql+pymysql://tests:tests@localhost:3306/Proxy"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manage = Manager(app)

manage.add_command("db", MigrateCommand)


class Proxy_db(db.Model):
    id = db.Column("id", INTEGER, primary_key=True)
    proxy_ip = db.Column("proxy_ip", VARCHAR(60), nullable=False)
    proxy_port = db.Column("proxy_port", INTEGER, nullable=False)
    proxy_country = db.Column("proxy_country", VARCHAR(255), nullable=False)
    proxy_type = db.Column("proxy_type", VARCHAR(255), nullable=False)
    addtime = db.Column("addtime", DATETIME, server_default=text('NOW()'))
    last_test_time = db.Column("last_test_time", DATETIME)
    proxy_status = db.Column("proxy_status", INTEGER, default='1')

    def __init__(self, **kwargs):
        self.proxy_ip = kwargs["proxy_ip"]
        self.proxy_port = kwargs["proxy_port"]
        self.proxy_country = kwargs["proxy_country"]
        self.proxy_type = kwargs["proxy_type"]

    @classmethod
    def select(cls, proxy_ip, proxy_port):
        query = cls.query.filter_by(proxy_ip=proxy_ip, proxy_port=proxy_port).count()
        if query:
            return True
        else:
            return False

    @classmethod
    def insert(cls, **kwargs):
        if cls.select(kwargs["proxy_ip"], kwargs["proxy_port"]):
            return {"message": "代理ip和端口已存在", "code": 0}, 200
        one = cls(**kwargs)
        db.session.add(one)
        db.session.commit()
        return {"message": "ok", "code": 1}, 200


parser = reqparse.RequestParser()
parser.add_argument("proxy_ip", type=str, required=True, help='代理ip', location='form')
parser.add_argument("proxy_port", type=int, required=True, help='代理端口', location='form')
parser.add_argument("proxy_country", type=str, required=True, help='代理ip城市', location='form')
parser.add_argument("proxy_type", type=str, required=True, help='代理ip类型', location='form')


class Proxy_API(Resource):
    def get(self):
        return "hello world"

    def post(self):
        args = parser.parse_args()
        result = Proxy_db.insert(**args)
        return result


api.add_resource(Proxy_API, "/api")


@manage.option('-m', '--mode', help='模式: gevent, debug')
def run(mode="debug"):
    if mode == "debug":
        @run_with_reloader
        def run_server():
            http_server = WSGIServer(('localhost', 5000), DebuggedApplication(app))
            http_server.serve_forever()
        run_server()
    elif mode == "gevent":
        http_server = WSGIServer(('localhost', 5000), app)
        http_server.serve_forever()
    else:
        raise "No {mode} mode!!"


if __name__ == '__main__':
    manage.run()
