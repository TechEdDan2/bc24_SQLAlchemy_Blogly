"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

# Connect the app to the db
db = SQLAlchemy()

# function to connect
def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_USER_IMG = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

# ----------- #
#   Models    #
# ----------- #
class User(db.Model):
    """User Schema Table"""

    __tablename__ = "users"

    # Attributes
    id = db.Column(db.Integer, 
                   primary_key = True,
                   autoincrement = True)
    
    name_first = db.Column(db.String(50),
                     nullable = False)
    
    name_last = db.Column(db.String(50),
                     nullable = False)
    
    user_image = db.Column(db.Text,
                        nullable = False,
                        default = DEFAULT_USER_IMG)

    posts = db.relationship("Post", backref="usr", cascade="all, delete-orphan")

    # Custom printout which overrides the original 
    def __repr__(self):
        """ 
        Returns a string representation of the User object. This method 
            provides a concise and informative representation of the User 
            object, useful for debugging and logging purposes.
        
        Returns:
            str: A string representation of the User object in the format:
                <User id=<id> first name = <name_first> Last Name = <name_last> Image URL = <user_image>> 
        """
        u = self
        return f"<User id={u.id} First Name = {u.name_first} Last Name = {u.name_last} Image URL = {u.user_image}>"

    @classmethod
    def get_all_users(cls):
        """ Retrieves a list of all active users """
        return cls.query.all()
    

    # Instance Methods
    @property
    def full_name(self):
        """ Returns the user's full name """
        return f"{self.name_first} {self.name_last}"
    
class Post(db.Model):
    """ Blog Post Schema"""

    __tablename__ = "posts"

     # Attributes
    id = db.Column(db.Integer, 
                   primary_key = True,
                   autoincrement = True)
    
    title = db.Column(db.Text,
                     nullable = False)
    
    content = db.Column(db.Text,
                     nullable = False)
    
    created_at = db.Column(db.DateTime,
                           nullable = False,
                           default=datetime.datetime.now) 
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship("Tag", secondary="posts_tags", back_populates="posts")

    @property
    def format_date(self):
        """
        Returns a formatted date 
        
        :return: A string representing the creation timestamp in the format 
         "Abbreviation of the Weekday and Month Day Year, Hour:Minute AM/PM" 
         (e.g., "Mon Jul 10 2024, 10:30 AM").

        """

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
class Tag(db.Model):
     """ Tag Schema"""
    
     __tablename__ = "tags"
     
     id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
     name = db.Column(db.Text,
                         nullable=False,
                         unique=True)
     posts = db.relationship("Post", secondary="posts_tags", back_populates="tags")
     
     def __repr__(self):
            ''' Returns a string representation of a Tag Object'''
            return f"<Tag id={self.id} name={self.name}>"
     
        


class PostTag(db.Model):
    """ M:M relationship between Posts and Tags this will be the through table"""

    __tablename__ = "posts_tags"
    post_id = db.Column(db.Integer, 
                            db.ForeignKey('posts.id'), 
                            primary_key=True)
        
    tag_id = db.Column(db.Integer, 
                           db.ForeignKey('tags.id'), 
                           primary_key=True)
        


