from ..db import db
from .catagory import Catagory


class Item(db.Model):
    """Represents an item type.""" 
    __tablename__ = 'item'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    catagory_id = db.Column(db.Integer(), db.ForeignKey('catagory.id'))
    catagory = db.relationship(Catagory, back_populates='items')
    __table_args__ = (db.UniqueConstraint('name', 'catagory_id'),)

    @property
    def catagory_name(self):
        """Name of item's catagory."""
        return self.catagory.name

    @catagory_name.setter
    def catagory_name(self, catagory_name):
        """Setter for catagory_name."""
        query = db.session.query(Catagory).filter(Catagory.name==catagory_name)
        catagory = query.one()
        self.catagory = catagory

    @property
    def dict(self):
        """Item instance as dict."""
        return {
            'id': self.id,
            'catagory_id': self.catagory_id,
            'name': self.name,
            'description': self.description
        }

    @classmethod
    def create(
        Cls, name, *, catagory=None, catagory_name=None, description=None
    ):
        """Add a new Item to database and return it."""
        if catagory and catagory_name:
            raise TypeError(
                'Must call with catagory or catagory_name, not both'
            )
        if not catagory:
            query = db.session.query(Catagory).filter(
                Catagory.name==catagory_name
            )
            catagory = query.one()
        instance = Cls(name=name, catagory=catagory, description=description)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def fetch_all(Cls):
        """Return all items."""
        return db.session.query(Cls).all()

    @classmethod
    def fetch_catagory(Cls, catagory_name):
        """Return all items with given catagory_name."""
        query = db.session.query(Catagory).filter(Catagory.name==catagory_name)
        catagory = query.one()
        query = db.session.query(Item)
        return query.filter(Cls.catagory==catagory).all()

    @classmethod
    def fetch_by_name_and_catagory_name(Cls, name, catagory_name):
        """Return item with given name and catagory_name."""
        query = db.session.query(Catagory).filter(Catagory.name==catagory_name)
        catagory = query.one()
        query = db.session.query(Item)
        filtered = query.filter(Cls.name==name, Cls.catagory==catagory)
        return filtered.one()

    def update(self, name=None, catagory_name=None, description=None):
        """Update given properties of item."""
        if name:
            self.name = name
        if catagory_name:
            self.catagory_name = catagory_name
        if description:
            self.description = description
        db.session.commit()

    def delete(self):
        """Remove an item."""
        db.session.delete(self)
        db.session.commit()