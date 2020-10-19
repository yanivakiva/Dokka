from dokka import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(1000))
    links = db.Column(db.String(1000))
    points = db.Column(db.String(1000))

    def __repr__(self):
        return f"Results('uuid: {self.uuid}', links: '{self.links}', points: {self.points})"


if __name__ == '__main__':
    pass
