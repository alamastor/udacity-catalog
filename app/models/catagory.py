from ..db import db


class Catagory(db.Model):
    """Represents a catagory of item."""
    __tablename__ = 'catagory'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(250), nullable=True, unique=True)
    items = db.relationship('Item')

    @property
    def dict(self):
        """Catagory instance as dict."""
        items = self.items
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.dict for item in items],
        }

    @classmethod
    def create(Cls, name):
        """Add a new catagory to database and return it."""
        instance = Cls(name=name)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def fetch_all(Cls):
        """Return all catagories."""
        return db.session.query(Cls).all()

    @classmethod
    def exists(Cls, name):
        """Return whether Catagory with given name exists in database."""
        q = db.session.query(Cls).filter(Cls.name==name)
        return db.session.query(q.exists()).one()[0]