import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    id = Column(Integer, primary_key=True)

class ClothingGroup(Base):
    __tablename__ = 'clothing_group'

    name = Column(String(40), nullable = False)
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class ClothingItem(Base):
    __tablename__ = 'clothing_item'

    name =  Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(120))
    size = Column(String(10))
    color = Column(String(20))
    price = Column(String(8))
    item_group_id = Column(Integer, ForeignKey('clothing_group.id'))
    clothing_group = relationship(ClothingGroup)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'price': self.price,
        }



engine = create_engine('sqlite:///clothingstorewithusers.db')
Base.metadata.create_all(engine)
