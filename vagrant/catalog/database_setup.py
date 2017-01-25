import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Catalog(Base):
    __tablename__ = 'catalog'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class CatalogItem(Base):
    __tablename__ = 'catalog_item'
    # no one can create a menu item w/o a name
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    description = Column(String(250))

    catalog_id = Column(Integer, ForeignKey('catalog.id'))


    catalog = relationship(Catalog)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id
        }

engine = create_engine('sqlite:///catalogapp.db')

Base.metadata.create_all(engine)
