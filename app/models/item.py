from ..db import db
from .catagory import Catagory


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    catagory_name = db.Column(db.String(250), db.ForeignKey('catagory.name'))
    catagory = db.relationship(Catagory)
    __table_args__ = (db.UniqueConstraint('name', 'catagory_name'),)

    @classmethod
    def create(
        Cls, name, *, catagory=None, catagory_name=None, description=None
    ):
        if catagory and catagory_name:
            raise TypeError(
                'Must call with catagory or catagory_name, not both'
            )
        if catagory:
            instance = Cls(
                name=name, catagory=catagory, description=description
            )
        else:
            instance = Cls(
                name=name, catagory_name=catagory_name, description=description
            )
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def fetch_all(Cls):
        return db.session.query(Cls).all()

    @classmethod
    def fetch_catagory(Cls, catagory_name):
        query = db.session.query(Item)
        return query.filter(Cls.catagory_name==catagory_name).all()

    @classmethod
    def fetch_by_name_and_catagory_name(Cls, name, catagory_name):
        query = db.session.query(Item)
        filtered = query.filter(
            Cls.name==name, Cls.catagory_name==catagory_name
        )
        return filtered.one()

    def update(self, name=None, catagory_name=None, description=None):
        if name:
            self.name = name
        if catagory_name:
            self.catagory_name = catagory_name
        if description:
            self.description = description
        db.session.commit()
