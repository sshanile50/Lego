from flask import Flask
from flask_restplus import Resource, Api
from enum import Enum
from apscheduler.schedulers.background import BackgroundScheduler
import models
import random


class Model(Enum):
    MEAN = 'mean'
    MEDIAN = 'median'


app = Flask(__name__)
api = Api(app)

parser = api.parser()
parser.add_argument('model', type=Model, choices=list(Model))
parser.add_argument('seconds', type=int)

scheduler = BackgroundScheduler()
scheduler.start()


def call_models_job(model):
    numbers = [random.random() for _ in range(10)]
    return models.mean(numbers) if model == Model.MEAN else models.median(numbers)


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


if __name__ == '__main__':
    app.run(debug=True)
