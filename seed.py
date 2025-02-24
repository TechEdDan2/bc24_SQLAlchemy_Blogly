""" Seed file to supply data for the User DB """

from models import User, db, Post, Tag, PostTag
from app import app

# create all tables
db.drop_all()
db.create_all()

# If table isn't empty, remove all data
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

# Add some starting User Data
test_user = User(name_first="Test", name_last="User", user_image="https://freerangestock.com/sample/167255/close-up-portrait-of-a-fluffy-brown-dog.jpg")
test_user2 = User(name_first="Python", name_last="Blogger", user_image="https://images.unsplash.com/photo-1669475616380-ecb159b790d4?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHByb2ZpbGUlMjBwaWN8ZW58MHx8MHx8fDA%3D")
test_user3 = User(name_first="Flask", name_last="Blogger")

# Add new objects to the session
db.session.add_all([test_user, test_user2, test_user3])

# Commit the data
db.session.commit()

# Add some tags
tag1 = Tag(name="Python")
tag2 = Tag(name="Flask")

# Add new objects to the session
db.session.add_all([tag1, tag2])

# Commit the data
db.session.commit()

# Add some tags for the posts
post1 = Post(title="First Post", content="This is a sample post about code", user_id=test_user.id)

# Add a post to a test user
db.session.add(post1)

# Commit the data
db.session.commit()

# Append the post with some tags
post1.tags.append(tag1)