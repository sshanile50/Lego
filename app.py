from flask import Flask
from flask_restplus import Resource, Api
from enum import Enum
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


@api.route('/activate')
class InvokeModels(Resource):
    def post(self):
        args = parser.parse_args()
        model = args['model']
        numbers = [random.random() for _ in range(10)]
        return models.mean(numbers) if model == Model.MEAN else models.median(numbers)


if __name__ == '__main__':
    app.run(debug=True)
