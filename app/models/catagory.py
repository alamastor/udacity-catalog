from sqlalchemy import Column, String

from ..db import db


class Catagory(db.Model):
    __tablename__ = 'catagory'
    name = Column(String(250), primary_key=True)

    @classmethod
    def create(Cls, name):
        instance = Cls(name=name)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def fetch_all(Cls):
        return db.session.query(Cls)
