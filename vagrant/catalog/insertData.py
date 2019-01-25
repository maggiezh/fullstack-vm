from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Category, Item, User

engine = create_engine('postgresql://catalog:catalog@localhost/catalogMngr')
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
User1 = User(username="Robo Barista", email="tinnyTim@udacity.com")
session.add(User1)
session.commit()
User2 = User(username="Maria Carey", email="mariacarey@udacity.com")
session.add(User2)
session.commit()
User3 = User(username="Twilio Who", email="twiliowho@udacity.com")
session.add(User3)
session.commit()

# Soccer
c1 = Category(name="Soccer")
session.add(c1)
session.commit()

item1 = Item(itemName="Soccer Cleats", description="A lightweight synthetic leather upper offers them enhanced touch and feel while a Phylon heel wedge and die-cut EVA sockliner delivers the ideal combination of padding and support for match long comfort. The soccer cleat has a rubber studded outsole that provides exceptional acceleration and traction on synthetic grass surfaces.", user_id=1, category_id=1)
session.add(item1)
session.commit()

item2 = Item(itemName="Jersey", description="This Soccer Jersey will keep you dry and comfortable from practice to the game. Constructed of sweat-wicking polyester fabric, this short sleeve features contrast side panels and neckline to add a pop of color to this simple design. Show off your pride and rush the field in style wearing this Soccer Jersey.", user_id=1, category_id=1)
session.add(item2)
session.commit()

item3 = Item(itemName="Two shinguards", description="For ultimate protection where you need it most, the Soccer Shin Guards boast a durable shell with ankle discs and foam backing that provides comfortable support and relief from impact.", user_id=1, category_id=1)
session.add(item3)
session.commit()

# Items for Basketball
c2 = Category(name="Basketball")
session.add(c2)
session.commit()

item1 = Item(itemName="Basketball Shorts", description="These lightweight bottoms feature climalite fabric, which wicks moisture away fast and keeps you dry. An stretchy waistband lends a secure fit around your hips, while side hand pockets keep small essentials close by. Feel like a champ whether you are under the hoop or not in the Basketball Shorts.", user_id=2, category_id=2)
session.add(item1)
session.commit()

item2 = Item(itemName="Scrimmage Vests", description="Ideal for team practice, this vest is reversible to split up your team, with a comfortable lightweight fit that is built to perform.", user_id=2, category_id=2)
session.add(item2)
session.commit()

item3 = Item(itemName="Mouthguard", description="Protection for basketball players, this Mouthguard has a Gel-Fit liner that custom molds to your teeth for a tight, comfortable fit. The Triple-Layer design features an integrated breathing channel and has a convertible tether that allows the mouthguard to be strapped or strapless. Crafted using a heavy-duty rubber Exoskeletal Shock Frame, the Gel Max Convertible Mouthguard offers the ultimate protection for any sport.", user_id=2, category_id=2)
session.add(item3)
session.commit()

item4 = Item(itemName="Headband", description="This headband is exactly what you need to keep your face cool and dry during any physical activity. Made from moisture wicking knitted Dri-FIT material, this headband will keep you cool while the intensity heats up. Show off your style with the reversible, two-colored design - perfect for home or away games.", user_id=2, category_id=2)
session.add(item4)
session.commit()

# Snowboarding
c3 = Category(name="Snowboarding")
session.add(c3)
session.commit()


item1 = Item(itemName="Snowboard", description="Snowboard is the cure for snow day boredom! Let your snow angel spend time decorating the snowboard however they'd like with permanent markers and stickers, then head for the snowy hills for a fun afternoon of snowboarding. The Snowboard is the perfect outlet for your favorite youngster's energy and creative talents.", user_id=3, category_id=3)
session.add(item1)
session.commit()

item2 = Item(itemName="Goggles", description="Made for a better view, these Goggles deliver awesome features with great performance. You will love the Expansion View technology for a wider field of view, while the thermoformed lenses team up with anti-fog coating for a clear, optimal view. A mid-size frame with plush foam keeps you comfortable all season long.", user_id=3, category_id=3)
session.add(item2)
session.commit()

# Hockey
c4 = Category(name="Hockey")
session.add(c4)
session.commit()


item1 = Item(itemName="Stick", description="Take to the streets this season with the ready-to-play stick. Made with multi-ply poplar vinyl wrapped shaft and molded blade construction, this Franklin Street Hockey Stick is built to last. The high-impact rigid polymer blade on the Franklin 1090 Street Hockey Stick can add pop and precision to your shots and passes while the full coverage vinyl graphic delivers on style and look.", user_id=1, category_id=4)
session.add(item1)
session.commit()

item2 = Item(itemName="Roller Hockey Skates", description="Built for comfort and maximum breathability during outdoor play, these Roller Hockey Skates feature a HI-LO chassis that combines speed and control for premium performance that lasts.", user_id=1, category_id=4)
session.add(item2)
session.commit()

# Frisbee
c5 = Category(name="Frisbee")
session.add(c5)
session.commit()

item1 = Item(itemName="Frisbee", description="Warm up your arm before the game and lead your team to victory with the Innova Pulsar Ultimate Disc. Designed for competition and recreation, the Pulsar is USA Ultimate approved for tournament play and is perfect for backyard freestyle throwing. Its durable and rigid DX plastic construction delivers solid performance round after round. Make big passes and get to the end zone during your next league game with the Innova Pulsar.", user_id=2, category_id=5)
session.add(item1)
session.commit()

item2 = Item(itemName="Disc Retriever", description="The easiest way to retrieve your sunken and missing discs is with the Dynamic Discs Golden Retriever Disc Retriever. This lightweight, compact device is perfectly packable, fitting in a pocket or your bag with ease. To use, you simply pull on the rope to unfold and toss into the water hazard, pulling on the rope as the retriever skims the bottom. You will save your favorite discs and maintain rapid gameplay with this unique, convenient device.", user_id=2, category_id=5)
session.add(item2)
session.commit()

# Baseball
c6 = Category(name="Baseball")
session.add(c6)
session.commit()

item1 = Item(itemName="Bat", description="The number one bat in college baseball, this bat has a two-piece design and explosive pop and superior balance.", user_id=3, category_id=6)
session.add(item1)
session.commit()

item2 = Item(itemName="Batting Gloves", description="Signature performance provides elite players the grip, comfort and support needed with these batting Gloves.", user_id=3, category_id=6)
session.add(item2)
session.commit()

print "Items are added!"