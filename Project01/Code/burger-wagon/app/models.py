from app import db


class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, title, price):
        self.title = title
        self.price = price

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize(self):
        """ Return object data in easily serializable format """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'date_created': self.date_created.isoformat()
        }
