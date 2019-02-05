from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_database_setup import  Base, ClothingGroup, ClothingItem
engine = create_engine('sqlite:///clothingstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

group1 = ClothingGroup(name = "Pants")

session.add(group1)
session.commit()

group2 = ClothingGroup(name = "Shoes")

session.add(group2)
session.commit()


group1 = ClothingGroup(name = "Hats")

session.add(group1)
session.commit()

print("now active")