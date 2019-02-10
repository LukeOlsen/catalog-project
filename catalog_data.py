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

group2 = ClothingGroup(name = "Shoes")

session.add(group2)
session.commit()

shoes1 =  ClothingItem(name = "Fancy Shoes", description = "These are shoes you want to wear to a nice event.", price="$60",
                        clothing_group=group2)

session.add(shoes1)
session.commit()

shoes2 =  ClothingItem(name = "Casual Shoes", description = "These are shoes you want to wear on a Sunday afternoon.", price="$30",
                        clothing_group=group2)

session.add(shoes2)
session.commit()

shoes3 =  ClothingItem(name = "Running Shoes", description = "These shoes are great for a jog.", price="$70",
                        clothing_group=group2)

session.add(shoes3)
session.commit()

group3 = ClothingGroup(name = "Shirts")

session.add(group3)
session.commit()

shirts1 =  ClothingItem(name = "Classic Tee", description = "A classic Tee. Always in style.", price="$15",
                        clothing_group=group3)

session.add(shirts1)
session.commit()

shirts2 =  ClothingItem(name = "Button down", description = "A solid business casual option.", price="$35",
                        clothing_group=group3)

session.add(shirts2)
session.commit()

shirts3 =  ClothingItem(name = "Long Sleeve Tee", description = "Something to wear when it starts getting colder.", price="$25",
                        clothing_group=group3)

session.add(shirts3)
session.commit()

group4 = ClothingGroup(name = "Outerware") 

session.add(group4)
session.commit()

outerware1 = ClothingItem(name = "Hoodie", description = "This is a classic take on a hoodie.", price="$30",
                            clothing_group = group4)
            
session.add(outerware1)
session.commit()

outerware2 = ClothingItem(name = "Trucker Jacket", description = "A jacket with more durability and water resistance.", price="$50",
                            clothing_group = group4)

session.add(outerware2)
session.commit()

outerware3 = ClothingItem(name = "Peacoat", description = "With formality and warmth.", price="$70",
                            clothing_group = group4)

session.add(outerware3)
session.commit()

print("Sample data now active!")
