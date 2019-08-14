from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Result(db.Model):
    result = db.Column(db.Float)
    model_name = db.Column(db.PickleType)
    time = db.Column(db.DateTime, primary_key=True)

    @property
    def serialize(self):
        return {
            "result": self.result,
            "model_name": self.model_name
        }
