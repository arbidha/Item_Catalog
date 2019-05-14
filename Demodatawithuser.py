from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///catalogitemwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@abc.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Category Soccer
category1 = Category(user_id=1, name="Soccer")

session.add(category1)
session.commit()

Item2 = CategoryItem(user_id=1, title="Soccer Ball", description="Earn the starting spot with help from the adidas X Glider II Soccer Ball, featuring a nylon-wound carcass and butyl bladder for ultimate durability and consistent performance.",
                     category=category1)

session.add(Item2)
session.commit()


Item1 = CategoryItem(user_id=1, title="Soccer Cleats", description="A Flyknit upper with all conditions control delivers touch, ball control and a locked down fit for peak performance.",
                     category=category1)

session.add(Item1)
session.commit()

print "Soccer added"

# Category Basketball
category2 = Category(user_id=1, name="Basketball")

session.add(category2)
session.commit()

Item3 = CategoryItem(user_id=1, title="Basketball", description="Durable composite leather construction provides a long-lasting grip Cross-hatched pebbled pattern prevents dust and dirt buildup",
                     category=category2)

session.add(Item3)
session.commit()

Item2 = CategoryItem(user_id=1, title="Hoops", description="Get years of fun playing against family and friends with the Lifetime 54 In-Ground Crank Basketball Hoop.",
                     category=category2)

session.add(Item2)
session.commit()


Item1 = CategoryItem(user_id=1, title="Basketball Shoes", description="These shoes will give energy return a new meaning with their Zoom turbo.",
                     category=category2)

session.add(Item1)
session.commit()

print "Basketball added"

# Category Baseball
category3 = Category(user_id=1, name="Baseball")

session.add(category3)
session.commit()


Item3 = CategoryItem(user_id=1, title="Helmet", description="Durable ABS plastic outer shell offers maximum protection climalite",
                     category=category3)

session.add(Item3)
session.commit()

Item2 = CategoryItem(user_id=1, title="Bat", description="Youth Bat a good option for players who value the traditional feel of a one-piece bat and the classic ping off a durable aluminum barrel.",
                     category=category3)

session.add(Item2)
session.commit()


Item1 = CategoryItem(user_id=1, title="Gloves & Mitts", description="Gloves feature a Pro Soft leather shell with American-made laces for longer lasting performance on the diamond.",
                     category=category3)

session.add(Item1)
session.commit()
print "Baseball added"

# Category Frisbee
category4 = Category(user_id=1, name="Frisbee")

session.add(category4)
session.commit()

# Category Snowboarding
category5 = Category(user_id=1, name="Snowboarding")

session.add(category5)
session.commit()

# Category Rock Climbing
category6 = Category(user_id=1, name="Rock Climbing")

session.add(category6)
session.commit()

# Category Foosball
category7 = Category(user_id=1, name="Rock Foosball")

session.add(category7)
session.commit()

# Category Skating  
category8 = Category(user_id=1, name="Skating")

session.add(category8)
session.commit()

# Category Hockey  
category9 = Category(user_id=1, name="Hockey")

session.add(category9)
session.commit()

print "Added all item"