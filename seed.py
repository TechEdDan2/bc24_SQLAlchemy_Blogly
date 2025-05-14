""" Seed file to supply data for the User DB """

from models import User, db, Post
from app import app

# create all tables
db.drop_all()
db.create_all()

# If table isn't empty, remove all data
User.query.delete()

# Add some starting User Data
test_user = User(name_first="Test", name_last="User")

# Add new objects to the session
db.session.add(test_user)

# Commit the data
db.session.commit()