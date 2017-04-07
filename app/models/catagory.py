from ..db import db


class Catagory(db.Model):
    __tablename__ = 'catagory'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(250), nullable=True, unique=True)
    items = db.relationship('Item')

    @property
    def dict(self):
        items = self.items
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.dict for item in items],
        }

    @classmethod
    def create(Cls, name):
        instance = Cls(name=name)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def fetch_all(Cls):
        return db.session.query(Cls).all()

    @classmethod
    def exists(Cls, name):
        q = db.session.query(Cls).filter(Cls.name==name)
        return db.session.query(q.exists()).one()[0]
