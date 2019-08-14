from flask import Flask, jsonify
from flask_restplus import Resource, Api
from enum import Enum
from apscheduler.schedulers.background import BackgroundScheduler
from dbmodels import db, Result
import models
import random
import datetime


class Model(str, Enum):
    MEAN = 'mean'
    MEDIAN = 'median'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:75210@localhost:5432/modelsResults'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)

with app.app_context():
    db.create_all()

parser = api.parser()
parser.add_argument('model', type=Model, choices=list(Model))
parser.add_argument('seconds', type=int)

scheduler = BackgroundScheduler()
scheduler.start()


def call_models_job(model):
    numbers = [random.random() for _ in range(10)]
    res = models.mean(numbers) if model == Model.MEAN else models.median(numbers)
    with app.app_context():
        db.session.add(Result(result=res, model_name=model, time=datetime.datetime.now()))
        db.session.commit()


@api.route('/activate')
class ActivateModels(Resource):
    def post(self):
        args = parser.parse_args()
        model = args['model']
        sec = args['seconds']
        scheduler.add_job(call_models_job, 'interval', seconds=sec, args=[model])


@api.route('/deactivate')
class DeactivateModels(Resource):
    def post(self):
        scheduler.remove_all_jobs()


@api.route('/stats')
class Stats(Resource):
    def get(self):
        results_list = Result.query.order_by(Result.time).all()
        return jsonify([i.serialize for i in results_list])


if __name__ == '__main__':
    app.run(debug=True)
