from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_database_setup import  Base, ClothingGroup, ClothingItem
engine = create_engine('sqlite:///clothingstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

group1 = ClothingGroup(name = "Pants")
group2 = ClothingGroup(name = "Shoes")

pants1 = ClothingItem(name = "Green Pants", description = "These are a very nice pair of green pants.", price = "$30", 
                        clothing_group=group1)

session.add(pants1)
session.commit()

pants2 = ClothingItem(name="Red Pants", description="These are a very nice pair of red pants.", price="$30",
                       clothing_group=group1)

session.add(pants2)
session.commit()

pants3 = ClothingItem(name="Black Pants", description="These are a very nice pair of black pants.", price="$30",
                       clothing_group=group1)

session.add(pants3)
session.commit()



print("now active")
