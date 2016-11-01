from ..db import db
from .catagory import Catagory


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    catagory_name = db.Column(db.String(250), db.ForeignKey('catagory.name'))
    catagory = db.relationship(Catagory)
    __table_args__ = (db.UniqueConstraint('name', 'catagory_name'),)

    @classmethod
    def create(Cls, name, *, catagory=None, catagory_name=None):
        if catagory and catagory_name:
            raise TypeError(
                'Must call with catagory or catagory_name, not both'
            )
        if catagory:
            instance = Cls(name=name, catagory=catagory)
        else:
            instance = Cls(name=name, catagory_name=catagory_name)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def fetch_all(Cls):
        return db.session.query(Cls)
