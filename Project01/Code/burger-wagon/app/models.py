from app import db


class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, title, price):
        self.title = title
        self.price = price

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """ Represents the object instance of the model whenever it is queries. """
        return '<title {}>'.format(self.title)
